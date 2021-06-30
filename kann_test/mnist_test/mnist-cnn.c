#include <unistd.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include "kann_extra/kann_data.h"
#include "kann.h"

#define U_HEIGHT 120
#define U_WIDTH 160

int classes_name[3] = {40, 21, 04};

typedef struct arrayCount
{
	int id;
	int correct_count;
	int wrong_count;
} arrayCount;

struct image
{
	char *content;
	int size;
};

arrayCount *nameArray = NULL;
void countToNameArray(int, int);
void printPercentage();
kann_data_t *createMyDynamicKann(char *filename, kann_data_t *);
// image getImage(char *imageName);
// image resizeImage(image img);

int nameArrayCount = 0;

int main(int argc, char *argv[])
{
	kann_t *ann;
	kann_data_t *x, *y;
	char *fn_in = 0, *fn_out = 0;
	// int c, mini_size = 64, max_epoch = 20, max_drop_streak = 10, seed = 131, n_h_fc = 128, n_h_flt = 32, n_threads = 1;
	int c, mini_size = 64, max_epoch = 10, max_drop_streak = 5, seed = 6745, n_threads = 4;
	int n_h_flt = 16;  // `filters` argument, the dimensionality of the output space (i.e. the number of output filters in the convolution)(https://keras.io/api/layers/convolution_layers/convolution2d/)
	int n_h_fc = 64;  // number of fully connected/dense units, as seen in Keras (https://www.tutorialspoint.com/keras/keras_dense_layer.htm)
	// Crashes at epoch 13
	// float lr = 0.001f, dropout = 0.2f, frac_val = 0.1f;
	float lr = 0.001f, dropout = 0.1f, frac_val = 0.1f;

	printf("Starting program..\n");
	system("pwd");
	fflush(stdout);
	while ((c = getopt(argc, argv, "i:o:m:h:f:d:s:t:v:")) >= 0)
	{
		if (c == 'i')
			fn_in = optarg;
		else if (c == 'o')
			fn_out = optarg;
		else if (c == 'm')
			max_epoch = atoi(optarg);
		else if (c == 'h')
			n_h_fc = atoi(optarg);
		else if (c == 'f')
			n_h_flt = atoi(optarg);
		else if (c == 'd')
			dropout = atof(optarg);
		else if (c == 's')
			seed = atoi(optarg);
		else if (c == 't')
			n_threads = atoi(optarg);
		else if (c == 'v')
			frac_val = atof(optarg);
	}

	if (argc - optind == 0 || (argc - optind == 1 && fn_in == 0))
	{
		FILE *fp = stdout;
		fprintf(fp, "Usage: mnist-cnn-gtsrb [-i model] [-o model] [-t nThreads] <x.knd> [y.knd]\n");
		return 1;
	}

	kad_trap_fe();
	kann_srand(seed);
	if (fn_in)
	{
		ann = kann_load(fn_in);
	}
	else
	{
		kad_node_t *t;
		// t = kad_feed(4, 1, 1, U_HEIGHT, U_WIDTH), t->ext_flag |= KANN_F_IN;
		// t = kad_relu(kann_layer_conv2d(t, n_h_flt, 8, 8, 1, 1, 0, 0)); // 3x3 kernel; 1x1 stride; 0x0 padding
		// t = kad_relu(kann_layer_conv2d(t, n_h_flt, 16, 16, 1, 1, 0, 0));
		// t = kad_max2d(t, 16, 16, 4, 4, 0, 0); // 2x2 kernel; 2x2 stride; 0x0 padding
		// t = kann_layer_dropout(t, dropout);
		// t = kann_layer_dense(t, n_h_fc);
		// t = kad_relu(t);
		// t = kann_layer_dropout(t, dropout);
		// ann = kann_new(kann_layer_cost(t, 3, KANN_C_CEB), 0);

		// LAST USED ARCHITECTURE
		// t = kad_feed(4, 1, 1, U_HEIGHT, U_WIDTH), t->ext_flag |= KANN_F_IN;
		// t = kad_relu(kann_layer_conv2d(t, n_h_flt, 9, 9, 1, 1, 0, 0)); // 3x3 kernel; 1x1 stride; 0x0 padding
		// t = kad_relu(kann_layer_conv2d(t, n_h_flt, 3, 3, 1, 1, 0, 0));
		// // t = kad_sigm(kann_layer_conv2d(t, n_h_flt, 3, 3, 1, 1, 0, 0));
		// t = kad_max2d(t, 4, 4, 4, 4, 0, 0); // 2x2 kernel; 2x2 stride; 0x0 padding
		// t = kann_layer_dropout(t, dropout);
		// t = kann_layer_dense(t, n_h_fc);
		// t = kad_relu(t);
		// t = kann_layer_dropout(t, dropout);
		// ann = kann_new(kann_layer_cost(t, 3, KANN_C_CEB), 0);

		t = kad_feed(4, 1, 1, U_HEIGHT, U_WIDTH), t->ext_flag |= KANN_F_IN;
		t = kad_relu(kann_layer_conv2d(t, n_h_flt, 3, 3, 1, 1, 0, 0)); // 3x3 kernel; 1x1 stride; 0x0 padding
		t = kad_relu(kann_layer_conv2d(t, n_h_flt, 2, 2, 1, 1, 0, 0));
		t = kad_max2d(t, 2, 2, 2, 2, 0, 0); // 2x2 kernel; 2x2 stride; 0x0 padding
		t = kann_layer_dropout(t, dropout);
		t = kann_layer_dense(t, n_h_fc);
		// t = kad_relu(t);
		t = kad_sigm(t);
		t = kann_layer_dropout(t, dropout);
		ann = kann_new(kann_layer_cost(t, 4, KANN_C_CEB), 0);

	}

	x = kann_data_read(argv[optind]);
	// kann_data_t *kdt = createMyDynamicKann(argv[optind], x);
	// assert(x->n_col == 28 * 28);
	y = argc - optind >= 2 ? kann_data_read(argv[optind + 1]) : 0;

	if (y)
	{ // training
		// assert(y->n_col == 3);
		if (n_threads > 1)
			kann_mt(ann, n_threads, mini_size);
		printf("Starting training..\n");
		fflush(stdout);
		kann_train_fnn1(ann, lr, mini_size, max_epoch, max_drop_streak, frac_val, x->n_row, x->x, y->x);
		if (fn_out)
			kann_save(fn_out, ann);
		kann_data_free(y);
	}
	else
	{ // applying
		// int i, j, n_out;
		// kann_switch(ann, 0);
		// n_out = kann_dim_out(ann);
		// assert(n_out == 10);
		// for (i = 0; i < x->n_row; ++i) {
		// 	const float *y;
		// y = kann_apply1(ann, x->x[i]);
		// 	if (x->rname) printf("%s\t", x->rname[i]);
		// 	for (j = 0; j < n_out; ++j) {
		// 		if (j) putchar('\t');
		// 		printf("%.3g", y[j] + 1.0f - 1.0f);
		// 	}
		// 	putchar('\n');
		// }
		kann_switch(ann, 0); // set the network for predicting
		long int mean_time = 0;
		for (int i = 0; i < x->n_row; i++)
		{
			const float *y;
			int n_out = kann_dim_out(ann);
			struct timeval start, stop;
			gettimeofday(&start, NULL);
			y = kann_apply1(ann, x->x[i]);
			gettimeofday(&stop, NULL);
			printf("Time: %lu us\n",(stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
			mean_time += (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec;
			// y = kann_apply1(ann, kdt->x[i]);
			if (x->rname)
				printf("%s\t", x->rname[i]); // index:className (ex. 1:40)

			char *_class = strchr(x->rname[i], ':');
			_class = _class + 1;
			int className = atoi(_class);
			fflush(stdout);
			int max_index = -1;
			float max = 0.0;
			for (int j = 0; j < n_out; j++)
			{
				printf("%.3g\t", y[j] + 1.0f - 1.0f);
				fflush(stdout);
				if (y[j] > max)
				{
					max = y[j];
					max_index = j;
				}
			}
			int asd = classes_name[max_index];
			countToNameArray(className, classes_name[max_index]);
			printf("\nPredicted: %d\n", classes_name[max_index]); // predicted output
		}

		printf("Mean time: %d\n", mean_time / x->n_row);
	}
	printPercentage();
	kann_data_free(x);
	kann_delete(ann);
	return 0;
}

void printPercentage()
{
	float percentage = 0.0;
	for (int i = 0; i < nameArrayCount; i++)
	{
		int total = nameArray[i].correct_count + nameArray[i].wrong_count;
		float num = nameArray[i].correct_count;
		percentage = (num / total) * 100;
		printf("Class: %d with %f confidence from %d samples.\n", nameArray[i].id, percentage, total);
		fflush(stdout);
	}
}

void countToNameArray(int given, int expected)
{
	int exists = 0;
	if (nameArray == NULL)
	{
		nameArray = (arrayCount *)malloc(sizeof(arrayCount));

		nameArray[0].id = expected;
		nameArray[0].correct_count = 0;
		nameArray[0].wrong_count = 0;

		nameArrayCount++;
	}
	else
	{
		for (int i = 0; i < nameArrayCount; i++)
		{
			if (nameArray[i].id == expected)
			{
				exists = 1;
				break;
			}
		}
		if (exists == 0) // if this id is not yet registered
		{
			nameArray = (arrayCount *)realloc(nameArray, sizeof(nameArray) + sizeof(arrayCount));

			nameArray[nameArrayCount].id = expected;
			nameArray[nameArrayCount].correct_count = 0;
			nameArray[nameArrayCount].wrong_count = 0;

			nameArrayCount++;
		}
	}

	for (int i = 0; i < nameArrayCount; i++)
	{
		if (nameArray[i].id == expected)
		{
			if (given == expected)
			{
				nameArray[i].correct_count++;
			}
			else
			{
				nameArray[i].wrong_count++;
			}
			break;
		}
	}
}

kann_data_t *createMyDynamicKann(char *filename, kann_data_t *kk)
{ // for testing purposes
	// read second row of the file in one variable
	// we suppose that we only have the data array
	int count = 128 * 128;
	int num_rows = 3;
	FILE *f = fopen(filename, "r");
	kann_data_t *ret = (kann_data_t *)calloc(1, sizeof(kann_data_t));
	float **x = (float **)malloc(sizeof(float *) * num_rows);
	for (int j = 0; j < num_rows; j++)
	{
		x[j] = (float *)malloc(sizeof(float) * count);
	}
	char *z;
	z = (char *)malloc(sizeof(char) * 400000);
	fgets(z, 400000, f); // get first line of comments; not needed further

	int row = 0;
	int column;
	float currentFloat;

	for (int lines = 0; lines < num_rows; lines++)
	{
		column = 0;
		fgets(z, 400000, f);
		z = z + 5; // skip "1:40\t"

		// use sscanf to read from string instead of tokenizing

		FILE *mem = fmemopen(z, strlen(z), "r");
		while (!feof(mem))
		{
			// fscanf(mem, "%f", &x[row][column++]);
			fscanf(mem, "%f", &currentFloat);
			x[row][column++] = currentFloat;
		}

		ret->n_row = row++;
		ret->n_col = count + 1; // we observe that this is how it is read with kann_data_read
		ret->x = x;
		ret->n_grp = 1;

		for (int i = 0; i < count; i++)
		{
			if (ret->x[lines][i] != kk->x[lines][i])
			{
				printf("Does not work. %f %f\n", ret->x[lines][i], kk->x[lines][i]);
			}
			fflush(stdout);
		}
	}

	return ret;
}

kann_data_t *createKannDataFromArray()
{
}
