# Code and examples for running DART at Wytham Woods

This repository presents code and examples for running DART to simulate surface reflectance at Wytham Woods. 

DART access and licencing can be found on the [DART](https://dart.omp.eu/#/) website.

The work package makes extensive use of the 3D models presented in [Realistic Forest Stand Reconstruction from Terrestrial LiDAR for Radiative Transfer Modelling](https://www.mdpi.com/2072-4292/10/6/933/htm) and [Chang Li](https://www.ugent.be/bw/environment/en/research/cavelab/contact/liu-chang)'s conversion of the models to `.obj` format (available from `add-DART` branch on the [wytham-woods-3d-model](https://bitbucket.org/tree_research/wytham_woods_3d_model/src/add_dart/) BitBucket). The Wytham.db sepctral database (in `DART_models/3D-explicit model/Spec/Wytham.db` of the repository) is also required to run the simulations. 

The Jupyter notebook runs through set-up and simulation scenarios as well as presenting Python tools to edit .xml and .obj files. 

Under the `dart` directory are files to run specific simulations; from a simple turbid medium model to full 3D explicit simulations. Under the `python` directory is code to manipulate the `.obj` files e.g. to remove leaves or to add extra branch cylinders.

A preliminary report oulining the results of this work package can be found in this [Google Doc](https://docs.google.com/document/d/1s9NbucR17Kpbeg3oip5GynxA-wM-zzzBTww6T5kO3mg/edit?usp=sharing).
