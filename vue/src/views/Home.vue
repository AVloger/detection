<template>
  <div>
    <h1 class="title">本系统使用Yolov5算法实现掘进工作的人员和前探梁的实时检测。</h1>
    <h1 class="t2">功能模块：</h1>
    <h4 style="margin-left: 40px">人员识别</h4>
    <div style="display:flex;justify:space-between; margin-left: 40px">
      <p style="width: 350px; margin-left: 15px;line-height:1.5em;">
        通过摄像头识别当前画面中的工作人员并且标识出来。同时，对敲帮问顶进行识别。</p>
      <div style="margin-left: 100px; margin-top: -30px">
        <img src="@/assets/worker.png" alt="">
      </div>
    </div>

    <h4 style="margin-left: 40px">前探梁识别</h4>
    <div style="display:flex;justify:space-between; margin-left: 40px">
      <p style="width: 350px; margin-left: 15px; line-height:1.5em;">
        通过摄像头识别当前画面中的前探梁个数并标识出来，通过统计识别出来的前探梁个数，数量不足发出报警。</p>
      <div style="margin-left: 100px; margin-top: -20px">
        <img src="@/assets/tanliang.png" alt="">
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