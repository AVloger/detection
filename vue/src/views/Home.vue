<template>
  <div>
    <h1 class="title">本系统使用Yolov5算法实现目标检测，在此基础上，分别使用单目测距和双目测距的方法进行测距。</h1>
    <h1 class="t2">应用前景：</h1>
    <h4 style="margin-left: 40px">移动机器人</h4>
    <div style="display:flex;justify:space-between; margin-left: 40px">
      <p style="width: 350px; margin-left: 15px;line-height:1.5em;">
        智能移动机器人需要根据自身的视觉系统感知周围环境，快速对环境中的多个目标进行检测、分辨其类别、测量其相对于自身的距离，从而为移动机器人的运动规划和自主运行奠定基础。</p>
      <div style="margin-left: 100px; margin-top: -30px">
        <img src="@/assets/robot.jpg" alt="">
      </div>
    </div>

    <h4 style="margin-left: 40px">自动驾驶</h4>
    <div style="display:flex;justify:space-between; margin-left: 40px">
      <p style="width: 350px; margin-left: 15px; line-height:1.5em;">
        驾驶员在驾驶汽车的过程中，通过视觉传感器代替人眼获取前方的环境信息，进而判断汽车前方目标的位置和距离信息，然后将前方存在的目标的相关信息提示给驾驶员，让驾驶员及时做出判断，由此可以在一定程度上降低交通事故发生的概率。因此对汽车的自动驾驶技术来说，研发车辆前方目标的检测与测距技术具有重要的意义。</p>
      <div style="margin-left: 100px; margin-top: -20px">
        <img src="@/assets/自动驾驶.png" alt="">
      </div>
    </div>


  </div>
</template>

<script>
export default {
  name: "Home"
}
</script>

<style scoped>
.title {
  margin-bottom: 10px;
}

.t2 {
  margin-bottom: 5px;
}

img {
  width: 300px;
}
</style>