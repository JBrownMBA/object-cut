# object-cut
[![HitCount](http://hits.dwyl.io/AlbertSuarez/object-cut.svg)](http://hits.dwyl.io/AlbertSuarez/object-cut)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/AlbertSuarez/object-cut)
[![GitHub stars](https://img.shields.io/github/stars/adriacabeza/Unnamed.svg)](https://GitHub.com/AlbertSuarez/object-cut/stargazers/)
[![GitHub forks](https://img.shields.io/github/forks/adriacabeza/Unnamed.svg)](https://GitHub.com/AlbertSuarez/object-cut/network/)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/AlbertSuarez/object-cut.svg)](https://github.com/AlbertSuarez/object-cut)

✂️ Cut an object of an image typing its name built in PyTorch Summer Hackathon

## Results

![](docs/images/test_cat_combined.png)
![](docs/images/test_cutlery_combined.png)
![](docs/images/test_dog_combined.png)
![](docs/images/test_pizza_combined.png)

## Architecture: Mask-RCNN

This tool works using a **Mask-RCNN** model trained with the **COCO dataset**, an extension of Faster-RCNN which adds the masks of each class that has been detected. 

<p align="center">
  <img src="https://cdn-images-1.medium.com/max/800/1*6MHxZVujW2W5khpQKCCDUw.png"
</p>
  
The model has two main stages. Firstly, using a **Region Proposal Network** (RPN) it generates several region proposals where there might be an object. Then, secondly, it predicts the class of the object, refines the bounding box and generates the mask in pixel level based on the first stage proposal. 
