# Tests

## Layers used

int c, mini_size = 32, max_epoch = 12, max_drop_streak = 5, seed = 6745, n_h_fc = 64, n_h_flt = 16, n_threads = 4;

t = kad_feed(4, 1, 3, 128, 128), t->ext_flag |= KANN_F_IN;
t = kad_relu(kann_layer_conv2d(t, n_h_flt, 9, 9, 1, 1, 0, 0)); // 3x3 kernel; 1x1 stride; 0x0 padding
t = kad_relu(kann_layer_conv2d(t, n_h_flt, 3, 3, 1, 1, 0, 0));
t = kad_max2d(t, 4, 4, 4, 4, 0, 0); // 2x2 kernel; 2x2 stride; 0x0 padding
t = kann_layer_dropout(t, dropout);
t = kann_layer_dense(t, n_h_fc);
t = kad_relu(t);
t = kann_layer_dropout(t, dropout);
ann = kann_new(kann_layer_cost(t, 3, KANN_C_CEB), 0);

For the 6 hours mnist-cnn-gtsrb-gray_shuffled_128.kan with more than 2 decimals:

kad_node_t *t;
t = kad_feed(4, 1, 1, 128, 128), t->ext_flag |= KANN_F_IN;
t = kad_relu(kann_layer_conv2d(t, n_h_flt, 8, 8, 1, 1, 0, 0)); // 3x3 kernel; 1x1 stride; 0x0 padding
t = kad_relu(kann_layer_conv2d(t, n_h_flt, 16, 16, 1, 1, 0, 0));
t = kad_max2d(t, 16, 16, 4, 4, 0, 0); // 2x2 kernel; 2x2 stride; 0x0 padding
t = kann_layer_dropout(t, dropout);
t = kann_layer_dense(t, n_h_fc);
t = kad_relu(t);
t = kann_layer_dropout(t, dropout);
ann = kann_new(kann_layer_cost(t, 3, KANN_C_CEB), 0);

## mnist-cnn-gtsrb-gray_v2_128.kan
-> Trained on: 128*128 gray without shuffled lines

On training dataset
1:40    0.792   0       0.052
40
2:21    0       0       1
04
3:04    0.0117  0.998   0
21

## mnist-cnn-gtsrb-gray_shuffled_128.kan
-> Trained on: 128*128 gray with shuffled lines. Precision is 2 decimals

1:04    0.0188  7.15e-07        0.993
04
2:40    0.0142  0.332   0.736
04
3:21    0.933   0.00121 0.0717
40

## mnist-cnn-gtsrb-gray_shuffled_128.kan with more than 2 decimals
DO NOT DELETE FFS. It took 6 hours to train
1:40    0.517   0.483   0.393
40
2:21    0.505   0.432   0.486
40
3:04    0.479   0.41    0.511
04

Turns out the data I was testing on was **NOT** the training data.
Even tough it classifies the training data correctly, it still takes
a lot of time to classify

## createMyDynamicKann 
On the same input as gtsrb-test-grayscale-128.knd-nomess, it result in 4(wrong),
where the data read from the file results in 40(correct)