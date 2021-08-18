#freeze_graph --input_graph=/home/sobey/tensorflowModel.pb --input_checkpoint=/home/sobey/tensorflowModel.ckpt --output_graph=/home/sobey/frozen_graph.pb --output_node_names=G_synthesis/images_out --input_binary=True
freeze_graph --input_graph=/home/sobey/tensorflowModel.pb --input_checkpoint=/home/sobey/tensorflowModel.ckpt --output_graph=/home/sobey/frozen_graph.pb --output_node_names=G_synthesis/images_out --input_binary=True
which python
