<template>

  <div>
    <div class="two_img">
      <img :src="uploadImg_left" style="width: 25%; height: auto; margin-right: 10vh;">
      <img :src="uploadImg_right" style="width: 25%; height: auto; margin-right: 10vh;">
    </div>

    <div>
      <div class="two_img">
        <img :src="detect_dis" style="width: 25%; height: auto; margin-right: 10vh;">
        <img :src="dianYun" style="width: 25%; height: auto; margin-right: 10vh;">
      </div>
    </div>

    <div class="btn">
      <el-upload
          action="http://localhost:9090/user/upload"
          :show-file-list="false"
          :on-success="handleUploadSuccess_left"
          style="display: inline-block">
        <el-button size="small" type="primary">上传左图</el-button>
      </el-upload>
      <el-button size="small" type="success" @click="detect">开始检测</el-button>
      <el-upload
          action="http://localhost:9090/user/upload"
          :show-file-list="false"
          :on-success="handleUploadSuccess_right"
          style="display: inline-block">
        <el-button size="small" type="primary">上传右图</el-button>
      </el-upload>
    </div>
  </div>


</template>

<script>
import backpack_dic from '@/assets/data/images/stereo/backpack/distance/dis.png'
import backpack_dianYun from '@/assets/data/images/stereo/backpack/dianYun/dianYun.png'
import bicycle_dic from '@/assets/data/images/stereo/bicycle/distance/dis.png'
import bicycle_dianYun from '@/assets/data/images/stereo/bicycle/dianYun/dianYun.png'
import motorcycle_dic from '@/assets/data/images/stereo/motorcycle/distance/dis.png'
import motorcycle_dianYun from '@/assets/data/images/stereo/motorcycle/dianYun/dianYun.png'
import bottle_dic from '@/assets/data/images/stereo/bottle/distance/dis.png'
import bottle_dianYun from '@/assets/data/images/stereo/bottle/dianYun/dianYun.png'
import laptop_dic from '@/assets/data/images/stereo/laptop/distance/dis.png'
import laptop_dianYun from '@/assets/data/images/stereo/laptop/dianYun/dianYun.png'

export default {
  name: "Stereo",
  data() {
    return {
      // 图片路径
      uploadImg_left: require('@/assets/upload.png'),
      uploadImg_right: require('@/assets/upload.png'),
      // detect_dis: require('@/assets/rocket.png'),
      // dianYun: require('@/assets/rocket.png'),
      detect_dis: null,
      dianYun: null,
      fileName: '',
      imgs: [
        backpack_dic,
        backpack_dianYun,
        bicycle_dic,
        bicycle_dianYun,
        motorcycle_dic,
        motorcycle_dianYun,
        bottle_dic,
        bottle_dianYun,
        laptop_dic,
        laptop_dianYun,
      ]

    }
  },
  methods: {
    handleUploadSuccess_left(res, file) {
      this.$message.success("上传成功")
      this.fileName = file.name
      this.uploadImg_left = URL.createObjectURL(file.raw);
    },
    handleUploadSuccess_right(res, file) {
      this.$message.success("上传成功")
      this.uploadImg_right = URL.createObjectURL(file.raw);
    },
    detect() {
      let newName = '../assets/data/images/monocular/detect/' + this.fileName
      let tmp = this.fileName.split('.')
      tmp = tmp[0]
      tmp = tmp[tmp.length - 1]
      this.detect_dis = this.imgs[tmp * 2]
      clearTimeout(this.timer);  //清除延迟执行
      this.timer = setTimeout(() => {   //设置延迟执行
        console.log('ok');
        this.dianYun = this.imgs[tmp * 2 + 1]
      }, 800);

    },
  }
}
</script>

<style scoped>
.two_img {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-top: 1vh;
}

.btn {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  margin-top: 5vh;
}

</style>