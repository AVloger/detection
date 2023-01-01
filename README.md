# Detection system for miner
## VUE of frontend
### Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
## JAVA of backend

## javaweb

```
java SpringbootApplication.java
```
## sql

the create sql file is located in javaweb/create.sql

## Flask of backend

```
python3 app.py
```

## how to train your model

### dependences

1、数据标注工具labelIMG

```
pip3 install labelimg
```

2、准备好的数据集图片

### train methods

1、标注数据，通过命令行窗口中输入labelimg弹出标注界面，并对图片进行逐一标注
2、将标注好的数据放在coco文件夹下
3、运行python train.py --data coco.yaml --cfg yolov5s.yaml --weights '' --batch-size 64
来训练模型，并在model-trainer/runs/train文件夹下得到best.pt文件
3、将best.pt放在back-end/weights目录下