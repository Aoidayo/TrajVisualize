<template>
  <div v-loading="is_loading">
    <el-row style="width: 98%; margin: 10px auto">
      <el-card
        shadow="never"
        style="margin-top: 10px; border: 2px solid rgb(125, 161, 81)"
      >
        <div slot="header" class="left-border">
          {{ title }}
        </div>
        <el-row>
          <!-- Test -->
          <!-- <el-col :span="24">
            <div style="width: 100px; margin: 10px auto">
              <div>Test</div>
              <div>选择轨迹</div>
            </div>
          </el-col> -->
          <el-col :span="3" style="margin-top: 6px"> 选择轨迹:</el-col>
          <el-col :span="6">
            <el-select
              v-model="selected_index"
              placeholder="请选择"
              @change="handleSelectChange"
            >
              <el-option
                v-for="index in query_list"
                :key="index"
                :label="index"
                :value="index"
              >
              </el-option>
            </el-select>
          </el-col>

          <el-col :offset="13" :span="2">
            <el-button @click="handleClick">查询</el-button>
          </el-col>
          <!-- <el-col :span="6">
            <el-button ></el-button>
          </el-col> -->
        </el-row>
        <el-row v-if="query_path != null" style="margin-top: 20px">
          <el-col :span="24">
            <iframe
              :src="query_path"
              scrolling="auto"
              frameborder="0"
              id="iframe4query"
              width="100%"
              height="400px"
            ></iframe>
          </el-col>
        </el-row>
      </el-card>
    </el-row>
    <el-row style="width: 98%; margin: 10px auto">
      <el-card
        shadow="never"
        style="margin-top: 10px; border: 2px solid rgb(125, 161, 81)"
      >
        <div slot="header" class="left-border">
          {{ maptitle }}
        </div>
        <el-row v-if="all_topk_path != null">
          <!-- All Topk -->
          <el-row>
            <el-row>
              <el-tag>所有TOPK</el-tag>
            </el-row>
            <el-row style="margin-top: 10px">
              <el-col :span="24">
                <iframe
                  :src="all_topk_path"
                  scrolling="auto"
                  frameborder="0"
                  id="iframe4topkall"
                  width="100%"
                  height="400px"
                ></iframe>
              </el-col>
            </el-row>
          </el-row>
          <el-row v-for="cnt in topks" :key="cnt">
            <el-row>
              <el-tag>TOP{{ cnt }}</el-tag>
            </el-row>
            <el-row style="margin-top: 10px">
              <el-col :span="24">
                <iframe
                  :src="handleTopCnt(cnt)"
                  scrolling="auto"
                  frameborder="0"
                  width="100%"
                  height="400px"
                ></iframe>
              </el-col>
            </el-row>
          </el-row>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-image :src="src"> </el-image>
          </el-col>
          <el-col :span="12">
            <div
              v-if="all_topk_path == null"
              style="width: 400px; margin: 40% auto; font-size: 40px"
            >
              结果PO在这里
            </div>
            <div v-else style="width: 400px; margin: 40% auto; font-size: 40px">
              到这里就结束了
            </div>
            <!-- <iframe
              src="http://localhost:8000/map"
              scrolling="auto"
              frameborder="0"
              id="iframe"
              width="100%"
              height="400px"
            ></iframe> -->
          </el-col>
        </el-row>
      </el-card>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "maptest",
  data() {
    return {
      title: "轨迹可视化",
      maptitle: "Traj4Map TOP5展示",
      openMap: null,
      src: "http://127.0.0.1:8000/image",
      query_list: [],
      selected_index: 9770,
      query_path: "http://127.0.0.1:8000/mapGenQuery/9770",
      is_loading: false,
      all_topk_path: null,
      topks: [1, 2, 3, 4, 5],
    };
  },
  mounted() {
    this.testconnect();
    // src = "http://127.0.0.1:8000/image";
    this.getqueries();
  },
  methods: {
    testconnect() {
      axios
        .get("http://127.0.0.1:8000")
        .then(function (response) {
          // 处理成功的情况
          console.log("Response from Flask:", response.data);
        })
        .catch(function (error) {
          // 处理错误的情况
          console.error("Error fetching data:", error);
        });
    },
    getqueries() {
      axios
        .get("http://127.0.0.1:8000/queries")
        .then((resp) => {
          console.log(resp.data);
          this.query_list = resp.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleSelectChange() {
      this.query_path = null;
      // this.is_loading = ture;
      axios
        .get("http://127.0.0.1:8000/queryMap/" + this.selected_index)
        .then((resp) => {
          console.log(resp);
          // this.is_loading = ture;
          this.query_path =
            "http://127.0.0.1:8000/mapGenQuery/" + this.selected_index;
          // this.is_loading = false;
        })
        .catch((err) => {
          console.log(err);
        });
      // var iframe = document.getElementById("iframe4query");
      // // 监听 iframe 的 load 事件
      // iframe.onload = function () {
      //   // iframe 加载完成后的处理逻辑
      //   console.log("iframe 加载完成");
      //   this.is_loading = false;
      // };
    },
    handleClick() {
      this.is_loading = true;
      this.all_topk_path = null;
      axios
        .get("http://127.0.0.1:8000/topk/" + this.selected_index)
        .then((resp) => {
          console.log(resp.data);
          this.all_topk_path = "http://127.0.0.1:8000/getTopkAll";
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          this.is_loading = false;
        });
    },
    handleTopCnt(cnt) {
      return "http://127.0.0.1:8000/getTopk/" + cnt;
    },
  },
};
</script>

<style scoped>
.left-border {
  border-left: 4px solid rgb(114, 150, 71);
  padding-left: 10px;
}
</style>