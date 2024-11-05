// Get input dataset for classification.
__hypermatrix__<N_SAMPLE, N_FEAT, float> train_dataset = ...;
int *train_labels = ...;
__hypermatrix__<N_TEST, N_FEAT, float> inference_dataset = ...;
int *true_inference_labels = ...;

// Train model, which is a set of representative hypervectors, one from each class.
__hypermatrix__<N_FEAT, DHV, float> rp_matrix = ...;
__hypermatrix__<N_CLASS, DHV, float> classes = 
	__hetero_hdc_training_loop(train_dataset, 
				   train_labels, 
				   rp_matrix,
				   EPOCHS);

// Infer class of unseen hypervectors by comparing against representatives.
int *pred_inference_labels = ...;
__hetero_hdc_inference_loop(inference_dataset, 
			    pred_inference_labels, 
			    rp_matrix, 
			    classes);

// Figure out how many classifications were correct.
int correct = 0;
for (int i = 0; i < N_TEST; ++i) {
	correct += pred_inference_labels[i] == 
		   true_inference_labels[i];
}
