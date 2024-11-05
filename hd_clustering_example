// Get input dataset for clustering.
__hypermatrix__<N_SAMPLE, N_FEAT, float> dataset = ...;

// The initial clusters are the first N_CLUSTER datapoints, encoded into a hypervector.
__hypermatrix__<N_FEAT, DHV, float> rp_matrix = ...;
__hypermatrix__<N_SAMPLE, DHV, float> encoded =
	__hetero_hdc_encoding_loop(dataset, rp_matrix);
__hypermatrix__<N_CLUSTER, DHV, float> clusters;
for (int i = 0; i < N_CLUSTER; ++i) {
	__hypervector__<DHV, float> encoded_hv =
		__hetero_hdc_get_matrix_row(encoded, i);
	__hetero_hdc_set_matrix_row(clusters, encoded_hv, i);
}

// Clustering is an iterative algorithm.
for (int i = 0; i < EPOCH; ++i) {
	// Determine which cluster each hypervector is in at first.
	int *clusters = ...;
	__hetero_hdc_inference_loop(dataset,
				    clusters,
				    rp_matrix,
				    clusters);

	// Determine the sum of all hypervectors in each cluster.
	__hypermatrix__<N_CLUSTER, DHV< float> clusters_tmp;
	for (int j = 0; j < N_SAMPLE; ++j) {
		int cluster = clusters[j];
		__hypervector__<DHV, float> update_hv =
			__hetero_hdc_get_matrix_row(clusters_tmp, cluster);
		__hypervector__<DHV, float> encoded_hv =
			__hetero_hdc_get_matrix_row(encoded, j);
		__hypervector__<DHV, float> sum_hv =
			__hetero_hdc_sum(update_hv, encoded_hv);
		__hetero_hdc_set_matrix_row(clusters_tmp, sum_hv, cluster);
	}

	// Copy clusters_tmp to clusters.
	for (int k = 0; k < N_CLUSTER; ++k) {
		__hypervector__<DHV, float> cluster_hv =
			__hetero_hdc_get_matrix_row(clusters_tmp, k);
		__hetero_hdc_set_matrix_row(clusters, cluster_hv, k);
	}
}
