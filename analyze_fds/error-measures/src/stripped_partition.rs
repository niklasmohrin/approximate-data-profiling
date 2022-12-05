use std::{
    collections::{HashMap, HashSet},
    mem,
};

use polars::prelude::*;
use rayon::prelude::*;

#[derive(Debug, Clone)]
pub struct StrippedPartition {
    pub columns: HashSet<String>,
    pub partitions: Vec<HashSet<usize>>,
}

impl StrippedPartition {
    pub fn new_initial_for(relation_size: usize) -> Self {
        Self {
            columns: HashSet::new(),
            partitions: vec![(0..relation_size).collect()],
        }
    }
    pub fn new_for_column_in(column_name: &str, relation: &DataFrame) -> anyhow::Result<Self> {
        let groups = relation
            .groupby([column_name])?
            .take_groups()
            .as_list_chunked();
        let non_trivial = groups.lst_lengths().gt(1);

        let partitions: Vec<HashSet<usize>> = groups
            .filter(&non_trivial)?
            .par_iter()
            .map(|index_series| {
                index_series
                    .expect("Index series should not be null")
                    .u32()
                    .expect("Index series should have u32 dtype.")
                    .into_no_null_iter()
                    .map(|index| index.try_into().unwrap())
                    .collect()
            })
            .collect();

        Ok(Self {
            columns: HashSet::from([column_name.to_owned()]),
            partitions,
        })
    }

    pub fn product_in(&self, other: &Self, relation: &DataFrame) -> Self {
        let mut partitions = Vec::new();

        let mut s = vec![HashSet::new(); self.partitions.len()];
        let mut t = vec![None; relation.height()];
        for (i, partition) in self.partitions.iter().enumerate() {
            for &tuple in partition.iter() {
                t[tuple] = Some(i);
            }
        }
        for partition in other.partitions.iter() {
            for &tuple in partition.iter() {
                if let Some(index) = t[tuple] {
                    s[index].insert(tuple);
                }
            }
            for &tuple in partition.iter() {
                if let Some(index) = t[tuple] {
                    let p = mem::take(&mut s[index]);
                    if p.len() >= 2 {
                        partitions.push(p);
                    }
                }
            }
        }

        Self {
            columns: self.columns.union(&other.columns).cloned().collect(),
            partitions,
        }
    }

    /// Number elements in each cluster in the partition - including clusters of size 1
    pub fn add_cluster_size_counts_to(
        &self,
        cluster_sizes: &mut HashMap<usize, usize>,
        relation_size: usize,
    ) {
        let mut total_seen_elements = 0;
        for partition in &self.partitions {
            total_seen_elements += partition.len();
            *cluster_sizes.entry(partition.len()).or_default() += 1;
        }
        *cluster_sizes.entry(1).or_default() += relation_size - total_seen_elements;
    }
}
