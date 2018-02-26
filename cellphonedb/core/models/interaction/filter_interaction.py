from cellphonedb.core.models.interaction import properties_interaction

import pandas as pd


def filter_by_multidata(multidata: pd.Series, interactions: pd.DataFrame):
    def filter(interaction):
        if interaction['multidata_1_id'] == multidata['id_multidata']:
            return True
        if interaction['multidata_2_id'] == multidata['id_multidata']:
            return True

        return False

    data_filtered = interactions[interactions.apply(filter, axis=1)]

    return data_filtered


def filter_by_multidatas(multidatas: pd.DataFrame, interactions: pd.DataFrame):
    interactions_filtered = pd.merge(multidatas, interactions, left_on='id_multidata', right_on='multidata_1_id')
    interactions_filtered = interactions_filtered.append(
        pd.merge(multidatas, interactions, left_on='id_multidata', right_on='multidata_2_id'))

    return interactions_filtered[interactions.columns.values]


def filter_by_min_score2(interactions, min_score2):
    filtered_interactions = interactions[interactions['score_2'] > min_score2]

    return filtered_interactions


def filter_receptor_ligand_interactions_by_receptor(interactions: pd.DataFrame, receptor: pd.Series) -> pd.DataFrame:
    result = interactions[
        interactions.apply(
            lambda interaction: properties_interaction.is_receptor_ligand_by_receptor(interaction, receptor), axis=1)]
    return result


def filter_receptor_ligand_ligand_receptor(interactions_expanded: pd.DataFrame, suffix=['_1', '_2']) -> pd.DataFrame:
    result = interactions_expanded[interactions_expanded.apply(
        lambda interaction: properties_interaction.is_receptor_ligand_or_ligand_receptor(interaction, suffix), axis=1)]

    return result


def filter_by_receptor_ligand_integrin(proteins: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame of enabled integrin interactions
    """
    print('Filtering by integrin')
    multidata_receptors = proteins[proteins['integrin_interaction']]

    receptor_interactions = pd.merge(multidata_receptors, interactions, left_on='id_multidata',
                                     right_on='multidata_1_id')
    enabled_interactions = pd.merge(proteins, receptor_interactions, left_on='id_multidata',
                                    right_on='multidata_2_id', suffixes=['_ligands', '_receptors'])

    receptor_interactions_inverted = pd.merge(multidata_receptors, interactions, left_on='id_multidata',
                                              right_on='multidata_2_id')

    enabled_interactions_inverted = pd.merge(proteins, receptor_interactions_inverted, left_on='id_multidata',
                                             right_on='multidata_1_id', suffixes=['_ligands', '_receptors'])

    enabled_interactions = enabled_interactions.append(enabled_interactions_inverted).reset_index(drop=True)

    enabled_interactions.drop_duplicates(inplace=True)

    return enabled_interactions


def filter_by_receptor_ligand_transmembrane(cluster_counts: pd.DataFrame,
                                            interactions_curated: pd.DataFrame) -> pd.DataFrame:
    multidata_receptors = cluster_counts[cluster_counts['is_cellphone_receptor']]
    multidata_ligands = cluster_counts[cluster_counts['is_cellphone_transmembrane_ligand']]

    receptor_interactions = pd.merge(multidata_receptors, interactions_curated, left_on='id_multidata',
                                     right_on='multidata_1_id')
    enabled_interactions = pd.merge(multidata_ligands, receptor_interactions, left_on='id_multidata',
                                    right_on='multidata_2_id', suffixes=['_ligands', '_receptors'])
    receptor_interactions_inverted = pd.merge(multidata_receptors, interactions_curated, left_on='id_multidata',
                                              right_on='multidata_2_id')
    enabled_interactions_inverted = pd.merge(multidata_ligands, receptor_interactions_inverted, left_on='id_multidata',
                                             right_on='multidata_1_id', suffixes=['_ligands', '_receptors'])
    enabled_interactions = enabled_interactions.append(enabled_interactions_inverted).reset_index(drop=True)

    enabled_interactions.drop_duplicates(['id_multidata_ligands', 'id_multidata_receptors'], inplace=True)
    return enabled_interactions


def filter_by_receptor_ligand_secreted(cluster_counts: pd.DataFrame,
                                       interactions: pd.DataFrame) -> pd.DataFrame:
    multidata_receptors = cluster_counts[cluster_counts['is_cellphone_receptor']]
    multidata_ligands = cluster_counts[cluster_counts['is_cellphone_secreted_ligand']]

    receptor_interactions = pd.merge(multidata_receptors, interactions, left_on='id_multidata',
                                     right_on='multidata_1_id')
    enabled_interactions = pd.merge(multidata_ligands, receptor_interactions, left_on='id_multidata',
                                    right_on='multidata_2_id', suffixes=['_ligands', '_receptors'])
    receptor_interactions_inverted = pd.merge(multidata_receptors, interactions, left_on='id_multidata',
                                              right_on='multidata_2_id')
    enabled_interactions_inverted = pd.merge(multidata_ligands, receptor_interactions_inverted, left_on='id_multidata',
                                             right_on='multidata_1_id', suffixes=['_ligands', '_receptors'])
    enabled_interactions = enabled_interactions.append(enabled_interactions_inverted).reset_index(drop=True)

    enabled_interactions.drop_duplicates(['id_multidata_ligands', 'id_multidata_receptors'], inplace=True)
    return enabled_interactions