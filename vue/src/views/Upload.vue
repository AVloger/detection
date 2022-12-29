<template>
  <div class="album albumvideo">
    <div>

      <div class="pic_img">
        <div class="pic_img_box">
          <el-upload class="avatar-uploader"
                     :action="uploadFileUrl"
                     v-bind:on-progress="uploadVideoProcess"
                     v-bind:on-success="handleVideoSuccess"
                     v-bind:on-error="handleVideoError"
                     v-bind:before-upload="beforeUploadVideo"
                     v-bind:show-file-list="false">


            <div class="avatar-icon-box">
              <img
                  v-if="videoForm.showVideoPath == ''"
                  class="avatar-icon imgess"
                  :src="require('@/assets/video-add.png')"
                  style="align-items: center; vertical-align: middle"
              />
              <video
                  v-else-if="videoForm.showVideoPath !== ''"
                  v-bind:src="videoForm.showVideoPath"
                  class="video-avatar"
                  :autoplay="true"
                  controls="controls"
                  muted
                  loop
              ></video>
              <el-progress v-if="videoFlag == true"
                           type="circle"
                           v-bind:percentage="videoUploadPercent"
                           style="margin-top:7px;"></el-progress>


            </div>
<!--            <video v-if="videoForm.showVideoPath !='' && !videoFlag"-->
<!--                   v-bind:src="videoForm.showVideoPath"-->
<!--                   class="avatar video-avatar"-->
<!--                   controls="controls">-->
<!--              您的浏览器不支持视频播放-->
<!--            </video>-->
<!--            <i v-else-if="videoForm.showVideoPath =='' && !videoFlag"-->
<!--               class="el-icon-plus avatar-uploader-icon"></i>-->

          </el-upload>

        </div>
      </div>
    </div>
    <p class="Upload_pictures">
      <span></span>
      <span>最多可以上传1个视频，建议大小50M，推荐格式mp4</span>
    </p>
  </div>
</template>

<script>

export default {
  name: "Upload",
  data() {
    return {
      uploadFileUrl: "http://127.0.0.1:5003/uploadVideo",
      videoFlag: false,
      //是否显示进度条
      videoUploadPercent: "",
      //进度条的进度，
      isShowUploadVideo: false,
      //显示上传按钮
      videoForm: {
        showVideoPath: ''
      }
    }
  },
  methods: {
    //上传前回调
    beforeUploadVideo(file) {
      var fileSize = file.size / 1024 / 1024 < 200;
      if (['video/mp4', 'video/ogg', 'video/flv', 'video/avi', 'video/wmv', 'video/rmvb', 'video/mov'].indexOf(file.type) == -1) {
        this.$message.info("请上传正确的视频格式");
        return false;
      }
      if (!fileSize) {
        this.$message.info("视频大小不能超过200MB");
        return false;
      }
      this.isShowUploadVideo = false;
    },
    //进度条
    uploadVideoProcess(event, file, fileList) {
      this.videoFlag = true;
      this.videoUploadPercent = file.percentage.toFixed(0) * 1;
    },
    handleVideoError(err, file, fileList){
      console.info("error")
      this.$message.info("上传视频失败")
    },

    //上传成功回调
    handleVideoSuccess(res, file) {
      this.$message.info("上传视频成功")
      this.isShowUploadVideo = true;
      this.videoFlag = false;
      this.videoUploadPercent = 0;

      //后台上传地址
      if (res.code == 200) {
        console.info(res.Data)
        this.videoForm.showVideoPath = res.Data;
      } else {
        this.$message.info(res.Message);
      }
    }
  }
}
</script>

<style scoped>

.avatar-uploader {
  height: 480px;
  width: 1000px;
  background-color: #313a69;
  border: 1px dashed #959bcb;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.avatar-uploader:hover .el-icon-circle-close {
  visibility: visible;
}
.video-avatar {
  width: 400px;
  height: 250px;

  z-index: 99;
}
.el-icon-circle-close {
  display: flex;
  float: right;
  margin-right: 6px;
  color: #959bcb;
  font-size: 22px;
  visibility: hidden;
}
.pic_img{
  display: block;
  width: 400px;
  /*height: 200px;*/
  float: left;
  position: relative;
}
.pic_img .pic_img_box
{
  display: block;
  position: relative;
  margin: 20px;
  width: 360px;
  height: 230px;
  background: #ffffff;
}
</style>