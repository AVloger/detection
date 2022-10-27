<template>
  <div class="myLive" id = myLive>
    <div class="top_button">
      <!--开启摄像头-->
      <Button
        v-if="isCameraFlag"
        type="primary"
        ghost
        @click="callCamera"
        style="text-align: center"
        >开始检测</Button
      >
      <!--关闭摄像头-->
      <Button
        v-else
        type="danger"
        ghost
        @click="closeCamera"
        style="text-align: center"
        >关闭检测</Button
      >
      <!--拍照-->
      <!-- <Button type="primary" @click="photograph"></Button> -->
    </div>
    <!--图片展示-->
    <video
      ref="video"
      width="500"
      height="376"
      autoplay
      class="mt20"
      style="background: #d9d9d9"
      v-show= "showtime"
    ></video>

    <div id="CT">
      <div id="CT_image">
        <el-card
          id="CT_image_1"
          class="box-card"
          style="
            border-radius: 8px;
            width: 800px;
            height: 360px;
            margin-bottom: -30px;
          "
        >
          <div class="demo-image__preview1">
            <canvas ref="canvas" width="500" height="376" v-if="isImg" class="image_1" ></canvas>
            <div class="img_info_1" style="border-radius: 0 0 5px 5px">
              <span style="color: white; letter-spacing: 6px">原始视频</span>
            </div>
          </div>
          <div class="demo-image__preview2">
            <img :src="yourBase64" alt="beachball" class="image_1" v-if="isImg" />
            <div class="img_info_1" style="border-radius: 0 0 5px 5px">
              <span style="color: white; letter-spacing: 4px">检测结果</span>
            </div>
          </div>
        </el-card>
      </div>
      <div id="info_patient">
        <!-- 卡片放置表格 -->
        <el-card style="border-radius: 8px">
          <div slot="header" class="clearfix">
            <span>检测目标</span>
          </div>
          <el-tabs v-model="activeName">
            <el-tab-pane label="检测到的目标" name="first">
              <!-- 表格存放特征值 -->
              <el-table
                :data="feature_list"
                height="390"
                border
                style="width: 800px; text-align: center"
                v-loading="loading"
                element-loading-text="数据正在处理中，请耐心等待"
                element-loading-spinner="el-icon-loading"
                lazy
                :row-class-name="tableRowClassName"
              >
                <el-table-column prop="object" label="目标类别" width="400px">
                  <template slot-scope="scope">
                    <span>{{ scope.row[2] }}</span>
                  </template>
                </el-table-column>

                <el-table-column prop="confidence" label="置信度" width="400px">
                  <template slot-scope="scope">
                    <span v-if = "scope.row[1]<40" style="color: red">{{ scope.row[1] }}</span>
                    <span v-else style="color: #2D2D3F">{{ scope.row[1] }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "myLive",
  data() {
    return {
        loading: false,
        activeName: "first",
        feature_list: [],
        feature_list_1: [],
        feat_list: [],
        showtime: false,
        yourBase64: "",
        isCameraFlag: true,
        base64: "",
        acc: "",
        str1: "",
        isImg: false,
    };
  },

  // 循环控制器
  mounted() {
    // this.timer = setInterval(this.photograph, 1000);
    this.timer = setInterval(() => {
      // 要执行的函数
      // console.log(this.isImg)
      if (this.isImg) {
        this.photograph();
      }
    }, 1000);
  },

  methods: {
    tableRowClassName({row, rowIndex}) {
      if (rowIndex === 0) {
        return 'warning-row';
      } else if (rowIndex === 3) {
        return 'success-row';
      }
      return '';
    },
    callCamera() {

      this.isImg = true
      this.isCamera = true;
      console.log(this.isCamera);
      // H5调用电脑摄像头API
      navigator.mediaDevices
        .getUserMedia({
          // audio: true, //开启音频
          video: true, //开启视频
        })
        .then((success) => {
          var videoTracks = success.getVideoTracks();
          this.$refs["video"].srcObject = success;
          this.isCameraFlag = false;
          // 实时拍照效果
          this.$refs["video"].play();
        })
        .catch((error) => {
          console.error("摄像头开启失败，请检查摄像头是否可用！");
          this.isCameraFlag = true;
        });
    },

    // 拍照
    async photograph() {
      let ctx = this.$refs["canvas"].getContext("2d");
      ctx.drawImage(this.$refs["video"], 0, 0, 500, 376);

      let img = this.$refs["canvas"].toDataURL("image/png").split('base64,')[1];
      var that = this;
      this.$http.post("/upload", {data:img}).then(function (response) {
        that.feature_list = [];
        that.yourBase64 = "data:image/jpeg;base64," + response.data.image_dev;
        that.feat_list = Object.keys(response.data.image_info);

        for (var i = 0; i < that.feat_list.length; i++) {
          response.data.image_info[that.feat_list[i]][2] = that.feat_list[i];
          that.feature_list.push(response.data.image_info[that.feat_list[i]]);
        }

      });
    },

    closeCamera() {
      this.isImg=false
      if (!this.$refs["video"].srcObject) return;
      let stream = this.$refs["video"].srcObject;
      let tracks = stream.getTracks();
      tracks.forEach((track) => {
        track.stop();
      });
      this.$refs["video"].srcObject = null;
      this.isCameraFlag = true;
    },
  },
};
</script>


<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 680px;
  height: 200px;
  border-radius: 8px;
  margin-top: -20px;
}
#myLive {
  width: 50%;
  height: 100%;
  background-color: #ffffff;
  margin: 15px auto;
  display: flex;
  flex-wrap: wrap;

  flex-direction: column;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */

}
#CT {
  display: flex;
  width: 100%;
  flex-wrap: wrap;
  flex-direction: column;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */

}

#CT_image_1 {
  width: 90%;
  height: 40%;
  margin: 0px auto;
  padding: 0px auto;
  align-self: center;
  border-radius: 4px;
}

#info_patient {
  width: 850px;
  height: 40%;
  margin-top: 40px;
  align-self: center;
  border-radius: 4px;
}
#CT_image {
  margin-bottom: 60px;

  margin-top: 5px;
}

.image_1 {
  width: 275px;
  height: 260px;
  background: #ffffff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.img_info_1 {
  height: 30px;
  width: 275px;
  text-align: center;
  background-color: #21b3b9;
  line-height: 30px;
}

.demo-image__preview1 {
  width: 250px;
  height: 290px;
  margin: 20px 40px;
  float: left;
}

.demo-image__preview2 {
  width: 250px;
  height: 290px;

  margin: 20px 460px;
  /* background-color: green; */
}


.block-sidebar .block-sidebar-item {
  font-size: 50px;
  color: lightblue;
  text-align: center;
  line-height: 50px;
  margin-bottom: 20px;
  cursor: pointer;
  display: block;
}

div {
  display: block;
}

.block-sidebar .block-sidebar-item:hover {
  color: #187aab;
}



</style>
