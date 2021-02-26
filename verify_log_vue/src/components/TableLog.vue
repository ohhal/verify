<template>
  <el-container>
    <el-header>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <el-date-picker
              v-model="dateValue"
              type="date"
              placeholder="选择日期"
              value-format="timestamp">
            </el-date-picker>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <el-input
              placeholder="请输入关键词用于搜索log中是否有此关键词"
              v-model="inputValue"
              clearable
            >
            </el-input>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="grid-content bg-purple">
            <el-button
              type="primary"
              @click="findButton()">查找</el-button>
          </div>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <div>
        <el-table
          v-loading="loading"
          :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
          border
          max-height="700"
          :default-sort="{prop: 'date', order: 'descending'}"
          style="width: 100%">
          <el-table-column
            label="id"
            fixed
            width="500">
            <template slot-scope="scope">
              <el-tag size="medium">{{ scope.row.id }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="表名"
            sortable
            width="500">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.table }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="日志最后更新时间"
            width="500">
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 10px">{{ timestampToTime(scope.row.time) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                @click="opnedialog(scope.row)">查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-main>
    <el-footer>
      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 40]"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next"
          :total="tableData.length"
          prev-text="上一页"
          next-text="下一页">
        </el-pagination>
      </div>
    </el-footer>

    <el-container>
      <div>
        <el-dialog title="打码日志" :visible.sync="dialogTableVisible">
          <el-table
            :data="gridData"
            border
            max-height="500"
            :default-sort="{prop: 'date', order: 'descending'}"
            style="width: 100%">
            <el-table-column label="id" width="150">
              <template slot-scope="scope">
                <span>{{ scope.row.id }}</span>
              </template>
            </el-table-column>
            <el-table-column label="接口" width="150">
              <template slot-scope="scope">
                <el-tag size="medium">{{ scope.row.api }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="时间" width="170">
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <span>{{ timestampToTime(scope.row.time) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="日志">
              <template slot-scope="scope">
                <span>{{ scope.row.log }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-dialog>
      </div>
    </el-container>
  </el-container>


</template>

<script>

export default {
  name: 'TableLog',
  data() {
    return {
      currentPage: 1, //默认显示页面为1
      pagesize: 10, //    每页的数据条数
      tableData: [],
      gridData: [],
      dialogTableVisible: false,
      serachurl: '/verify/log/serach',
      idurl: '/verify/log',
      inputValue: '',
      dateValue: '',
      state: '',
    };
  },
  created() {
    this.getdata()
  },
  methods: {
    // 根据条件查找所有的id
    getdata(inputData,dateData) {
      const that = this;
      this.$ajax({
        method: 'POST',
        url: that.serachurl,
        data: {
          'search':inputData,
          'date':dateData
        },
        dataType:'json',
      }).then(function (response) {
        that.tableData = response.data['msg']
      },function(){
        that.$message.error('日志接口请求失败');
      })
    },
    // 每页下拉显示数据
    handleSizeChange: function (size) {
      this.pagesize = size;
    },
    // 点击第几页
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    // 打开显示日志详情界面
    opnedialog(row) {
      this.dialogTableVisible = true
      this.getdata_id(row.valueOf().id)
    },
    // 根据id 获取日志
    getdata_id(_id) {
      const that = this;
      this.$ajax({
        method: 'POST',
        url: that.idurl,
        data: {
          "id": _id,
        }
      }).then(function (response) {
        that.gridData = response.data['msg']
      },function(){
        that.$message.error('日志接口请求失败');
      })
    },
    // 时间格式化
    timestampToTime(timestamp) {
      var date = new Date(timestamp / 1000);//时间戳为16位
      let y = date.getFullYear();
      let MM = date.getMonth() + 1;
      MM = MM < 10 ? ('0' + MM) : MM;
      let d = date.getDate();
      d = d < 10 ? ('0' + d) : d;
      let h = date.getHours();
      h = h < 10 ? ('0' + h) : h;
      let m = date.getMinutes();
      m = m < 10 ? ('0' + m) : m;
      let s = date.getSeconds();
      s = s < 10 ? ('0' + s) : s;
      return y + '-' + MM + '-' + d + ' ' + h + ':' + m + ':' + s;
    },
    findButton(){
      this.getdata(this.inputValue,this.dateValue)
    }
  },
}
</script>
