from __future__ import division, unicode_literals, print_function

import numpy as np
from numpy.linalg import norm
from scipy.interpolate import griddata

from matminer.featurizers.base import BaseFeaturizer
from matminer.featurizers.site import OPSiteFingerprint
from matminer.distance_metrics.site import get_tet_bcc_motif
from pymatgen import Spin
from pymatgen.electronic_structure.bandstructure import BandStructure, \
    BandStructureSymmLine
from pymatgen.electronic_structure.dos import CompleteDos
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

__author__ = 'Anubhav Jain <ajain@lbl.gov>'


class BranchPointEnergy(BaseFeaturizer):
    def __init__(self, n_vb=1, n_cb=1, calculate_band_edges=True):
        """
        Calculates the branch point energy and (optionally) an absolute band
        edge position assuming the branch point energy is the center of the gap

        Args:
            n_vb: (int) number of valence bands to include in BPE calc
            n_cb: (int) number of conduction bands to include in BPE calc
            calculate_band_edges: (bool) whether to also return band edge
                positions
        """
        self.n_vb = n_vb
        self.n_cb = n_cb
        self.calculate_band_edges = calculate_band_edges

    def featurize(self, bs, target_gap=None):
        """
        Args:
            bs: (BandStructure) Uniform (not symm line) band structure

        Returns:
            (int) branch point energy on same energy scale as BS eigenvalues
        """
        if bs.is_metal():
            raise ValueError("Cannot define a branch point energy for metals!")

        if isinstance(bs, BandStructureSymmLine):
            raise ValueError("BranchPointEnergy works only with uniform (not "
                             "line mode) band structures!")

        total_sum_energies = 0
        num_points = 0

        kpt_wts = SpacegroupAnalyzer(bs.structure).get_kpoint_weights(
            [k.frac_coords for k in bs.kpoints])

        for spin in bs.bands:
            for kpt_idx in range(len(bs.kpoints)):
                vb_energies = []
                cb_energies = []
                for band_idx in range(bs.nb_bands):
                    e = bs.bands[spin][band_idx][kpt_idx]
                    if e > bs.efermi:
                        cb_energies.append(e)
                    else:
                        vb_energies.append(e)
                vb_energies.sort(reverse=True)
                cb_energies.sort()
                total_sum_energies += (sum(
                    vb_energies[0:self.n_vb]) / self.n_vb + sum(
                    cb_energies[0:self.n_cb]) / self.n_cb) * kpt_wts[
                                          kpt_idx] / 2

                num_points += kpt_wts[kpt_idx]

        bpe = total_sum_energies / num_points

        if not self.calculate_band_edges:
            return [bpe]

        vbm = bs.get_vbm()["energy"]
        cbm = bs.get_cbm()["energy"]
        shift = 0
        if target_gap:
            # for now, equal shift to VBM / CBM
            shift = (target_gap - (cbm - vbm)) / 2

        return [bpe, (vbm - bpe - shift), (cbm - bpe + shift)]

    def feature_labels(self):

        return ["branch_point_energy", "vbm_absolute",
                "cbm_absolute"] if self.calculate_band_edges else [
            "branch point energy"]

    def citations(self):
        return ["@article{Schleife2009, author = {Schleife, A. and Fuchs, F. "
                "and R{\"{o}}dl, C. and Furthm{\"{u}}ller, J. and Bechstedt, "
                "F.}, doi = {10.1063/1.3059569}, isbn = {0003-6951}, issn = "
                "{00036951}, journal = {Applied Physics Letters}, number = {1},"
                " pages = {2009--2011}, title = {{Branch-point energies and "
                "band discontinuities of III-nitrides and III-/II-oxides "
                "from quasiparticle band-structure calculations}}, volume = "
                "{94}, year = {2009}}"]

    def implementors(self):
        return ["Anubhav Jain"]


class BandFeaturizer(BaseFeaturizer):
    """
    Featurizes a pymatgen band structure object.
    Args:
        kpoints ([1x3 numpy array]): list of fractional coordinates of
                k-points at which energy is extracted.
        find_method (str): the method for finding or interpolating for energy
            at given kpoints. It does nothing if kpoints is None.
            options are:
                'nearest': the energy of the nearest available k-point to
                    the input k-point is returned.
                'linear': the result of linear interpolation is returned
                see the documentation for scipy.interpolate.griddata
        nbands (int): the number of valence/conduction bands to be featurized
    """

    def __init__(self, kpoints=None, find_method='nearest', nbands = 2):
        self.kpoints = kpoints
        self.find_method = find_method
        self.nbands = nbands

    def featurize(self, bs):
        """
        Args:
            bs (pymatgen BandStructure or BandStructureSymmLine or their dict):
                The band structure to featurize. To obtain all features, bs
                should include the structure attribute.

        Returns:
             ([float]): a list of band structure features. If not bs.structure,
                features that require the structure will be returned as NaN.
            List of currently supported features:
                band_gap (eV): the difference between the CBM and VBM energy
                is_gap_direct (0.0|1.0): whether the band gap is direct or not
                direct_gap (eV): the minimum direct distance of the last
                    valence band and the first conduction band
                p_ex1_norm (float): k-space distance between Gamma point
                    and k-point of VBM
                n_ex1_norm (float): k-space distance between Gamma point
                    and k-point of CBM
                p_ex1_degen: degeneracy of VBM
                n_ex1_degen: degeneracy of CBM
                if kpoints is provided (e.g. for kpoints == [[0.0, 0.0, 0.0]]):
                    n_0.0;0.0;0.0_en: (energy of the first conduction band at
                        [0.0, 0.0, 0.0] - CBM energy)
                    p_0.0;0.0;0.0_en: (energy of the last valence band at
                        [0.0, 0.0, 0.0] - VBM energy)
        """
        if isinstance(bs, dict):
            bs = BandStructure.from_dict(bs)
        if bs.is_metal():
            raise ValueError("Cannot featurize a metallic band structure!")
        bs_kpts = [k.frac_coords for k in bs.kpoints]
        cvd = {'p': bs.get_vbm(), 'n': bs.get_cbm()}
        for itp, tp in enumerate(['p', 'n']):
            cvd[tp]['k'] = bs.kpoints[cvd[tp]['kpoint_index'][0]].frac_coords
            cvd[tp]['bidx'], cvd[tp]['sidx'] = \
                self.get_bindex_bspin(cvd[tp], is_cbm=bool(itp))
            cvd[tp]['Es'] = np.array(bs.bands[cvd[tp]['sidx']][cvd[tp]['bidx']])
        band_gap = bs.get_band_gap()

        # featurize
        self.feat = {}
        self.feat['band_gap'] = band_gap['energy']
        self.feat['is_gap_direct'] = band_gap['direct']
        self.feat['direct_gap'] = min(cvd['n']['Es'] - cvd['p']['Es'])
        if self.kpoints:
            obands = {'n': [], 'p': []}
            for spin in bs.bands:
                for band_idx in range(bs.nb_bands):
                    if max(bs.bands[spin][band_idx]) < bs.efermi:
                        obands['p'].append(bs.bands[spin][band_idx])
                    if min(bs.bands[spin][band_idx]) > bs.efermi:
                        obands['n'].append(bs.bands[spin][band_idx])
            bands = {tp: np.zeros((len(obands[tp]), len(self.kpoints))) for tp in ['p', 'n']}
            for tp in ['p', 'n']:
                for ib, ob in enumerate(obands[tp]):
                    bands[tp][ib, :] = griddata(points=np.array(bs_kpts),
                                   values=np.array(ob) - cvd[tp]['energy'],
                                   xi=self.kpoints, method=self.find_method)
                for ik, k in enumerate(self.kpoints):
                    sorted_band = np.sort(bands[tp][:, ik])
                    if tp == 'p':
                        sorted_band = sorted_band[::-1]
                    for ib in range(self.nbands):
                        k_name = '{}_{};{};{}_en{}'.format(tp, k[0], k[1], k[2], ib+1)
                        try:
                            self.feat[k_name] = sorted_band[ib]
                        except IndexError:
                            self.feat[k_name] = float('NaN')

        for tp in ['p', 'n']:
            self.feat['{}_ex1_norm'.format(tp)] = norm(cvd[tp]['k'])
            if bs.structure:
                self.feat['{}_ex1_degen'.format(tp)] = \
                    bs.get_kpoint_degeneracy(cvd[tp]['k'])
            else:
                self.feat['{}_ex1_degen'.format(tp)] = float('NaN')
        return list(self.feat.values())

    def feature_labels(self):
        return list(self.feat.keys())

    @staticmethod
    def get_bindex_bspin(extremum, is_cbm):
        """
        Returns the band index and spin of band extremum

        Args:
            extremum (dict): dictionary containing the CBM/VBM, i.e. output of
                Bandstructure.get_cbm()
            is_cbm (bool): whether the extremum is the CBM or not
        """

        idx = int(is_cbm) - 1  # 0 for CBM and -1 for VBM
        try:
            bidx = extremum["band_index"][Spin.up][idx]
            bspin = Spin.up
        except IndexError:
            bidx = extremum["band_index"][Spin.down][idx]
            bspin = Spin.down
        return bidx, bspin

    def citations(self):
        return ['@article{in_progress, title={{In progress}} year={2017}}']

    def implementors(self):
        return ['Alireza Faghaninia', 'Anubhav Jain']


class DOSFeaturizer(BaseFeaturizer):
    """
    Featurizes a pymatgen dos object.
    """

    def __init__(self, contributors=1, significance_threshold=0.1,
                 coordination_features=True, energy_cutoff=0.5,
                 sampling_resolution=100, gaussian_smear=0.1):
        """
        Args:
            contributors (int):
                Sets the number of top contributors to the DOS that are
                returned as features. (i.e. contributors=1 will only return the
                main cb and main vb orbital)
            significance_threshold (float):
                Sets the significance threshold for orbitals in the DOS.
                Does not impact the number of contributors returned. Only
                determines the feature value xbm_significant_contributors.
                The threshold is a fractional value between 0 and 1.
            coordination_features (bool):
                If true, the coordination environment of the PDOS contributors
                will also be returned. Only limited environments are currently
                supported. If the environment is neither, "unrecognized" will
                be returned.
            energy_cutoff (float in eV):
                The extent (into the bands) to sample the DOS
            sampling_resolution (int):
                Number of points to sample DOS
            gaussian_smear (float in eV):
                Gaussian smearing (sigma) around each sampled point in the DOS
        """
        self.contributors = contributors
        self.significance_threshold = significance_threshold
        self.coordination_features = coordination_features
        self.energy_cutoff = energy_cutoff
        self.sampling_resolution = sampling_resolution
        self.gaussian_smear = gaussian_smear

    def featurize(self, dos):
        """
        Args:
            dos (pymatgen CompleteDos or their dict):
                The density of states to featurize. Must be a complete DOS,
                (i.e. contains PDOS and structure, in addition to total DOS)
                and must contain the structure.

        Returns:
            xbm_score_i (float): fractions of ith contributor orbital
            xbm_location_i (str): cartesian coordinate of ith contributor.
                For example, '0.0;0.0;0.0' if Gamma
            xbm_specie_i: (str) elemental specie of ith contributor (ex: 'Ti')
            xbm_character_i: (str) orbital character of ith contributor (s p d or f)
            xbm_coordination_i: (str) the coordination geometry that the ith
                contributor orbital reside in. (the coordination environment
                of the site the orbital is associated with)
            xbm_nsignificant: (int) the number of orbitals with contributions
                above the significance_threshold
        """

        if isinstance(dos, dict):
            dos = CompleteDos.from_dict(dos)
        if dos.structure is None:
            raise ValueError('The input dos must contain the structure.')
        orbscores = get_cbm_vbm_scores(dos,
                self.coordination_features, self.energy_cutoff,
                self.sampling_resolution, self.gaussian_smear)
        self.feat = {}
        for ex in ['cbm', 'vbm']:
            orbscores.sort(key=lambda x: x['{}_score'.format(ex)], reverse=True)
            scores = np.array([s['{}_score'.format(ex)] for s in orbscores])
            self.feat['{}_nsignificant'.format(ex)] = len(scores[scores>self.significance_threshold])
            i = 0
            while i < self.contributors:
                sd = orbscores[i]
                if i < len(orbscores):
                    for p in ['character', 'specie', 'coordination']:
                        self.feat['{}_{}_{}'.format(ex, p, i + 1)] = sd[p]
                    self.feat['{}_location_{}'.format(ex, i+1)] = '{};{};{}'.format(
                        sd['location'][0], sd['location'][1], sd['location'][2])
                    self.feat['{}_score_{}'.format(ex, i+1)] = float(sd['{}_score'.format(ex)])
                else:
                    for p in ['{}_score'.format(ex), 'character', 'specie',
                              'coordination', 'location']:
                        self.feat['{}_{}_{}'.format(ex, p, i+1)] = float('NaN')
                i += 1
        return list(self.feat.values())

    def feature_labels(self):
        return list(self.feat.keys())

    def implementors(self):
        return ['Maxwell Dylla', 'Alireza Faghaninia', 'Anubhav Jain']


def get_cbm_vbm_scores(dos, coordination_features, energy_cutoff,
                       sampling_resolution, gaussian_smear):
    """
    Args:
        dos (pymatgen CompleteDos or their dict):
            The density of states to featurize. Must be a complete DOS,
            (i.e. contains PDOS and structure, in addition to total DOS)
        coordination_features (bool):
            if true, will also return the coordination enviornment of the
            PDOS features
        energy_cutoff (float in eV):
            The extent (into the bands) to sample the DOS
        sampling_resolution (int):
            Number of points to sample DOS
        gaussian_smear (float in eV):
            Gaussian smearing (sigma) around each sampled point in the DOS
    Returns:
        orbital_scores [(dict)]:
            A list of how much each orbital contributes to the partial
            density of states up to energy_cutoff. Dictionary items are:
            .. cbm_score: (float) fractional contribution to conduction band
            .. vbm_score: (float) fractional contribution to valence band
            .. species: (pymatgen Specie) the Specie of the orbital
            .. character: (str) is the orbital character s, p, d, or f
            .. location: [(float)] cartesian coordinates of the orbital
            .. coordination (str) optional-coordination environment from op
                                    site feature vector
    """

    cbm, vbm = dos.get_cbm_vbm(tol=0.01)
    structure = dos.structure
    sites = structure.sites

    orbital_scores = []
    for i in range(0, len(sites)):

        # if you desire coordination environment as feature
        if coordination_features:
            geometry = get_tet_bcc_motif(structure, i)

        site = sites[i]
        proj = dos.get_site_spd_dos(site)
        for orb in proj:
            # calculate contribution
            energies = [e for e in proj[orb].energies]
            smear_dos = proj[orb].get_smeared_densities(gaussian_smear)
            dos_up = smear_dos[Spin.up]
            dos_down = smear_dos[Spin.down] if Spin.down in smear_dos \
                else smear_dos[Spin.up]
            dos_total = [sum(id) for id in zip(dos_up, dos_down)]

            vbm_score = 0
            vbm_space = np.linspace(vbm, vbm - energy_cutoff,
                                    num=sampling_resolution)
            for e in vbm_space:
                vbm_score += np.interp(e, energies, dos_total)

            cbm_score = 0
            cbm_space = np.linspace(cbm, cbm + energy_cutoff,
                                    num=sampling_resolution)
            for e in cbm_space:
                cbm_score += np.interp(e, energies, dos_total)

            # add orbital scores to list
            orbital_score = {
                'cbm_score': cbm_score,
                'vbm_score': vbm_score,
                'specie': str(site.specie),
                'character': str(orb),
                'location': list(site.coords)}
            if coordination_features:
                orbital_score['coordination'] = geometry
            orbital_scores.append(orbital_score)

    # normalize by total contribution
    total_cbm = sum([orbital_scores[i]['cbm_score'] for i in
                     range(0, len(orbital_scores))])
    total_vbm = sum([orbital_scores[i]['vbm_score'] for i in
                     range(0, len(orbital_scores))])
    for orbital in orbital_scores:
        orbital['cbm_score'] = orbital['cbm_score'] / total_cbm
        orbital['vbm_score'] = orbital['vbm_score'] / total_vbm

    return orbital_scores