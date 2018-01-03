<template>
    <div class="container margin10">
        <table class="ui celled table">
            <thead>
            <tr v-if="outSize">
                <th colspan="6">
                    <Pagination :conf="conf"></Pagination>
                </th>
            </tr>
            <tr>
                <th>
                    <button class="ui labeled icon button orange" @click="create()">
                        <i class="plus icon white"></i>
                        新建
                    </button>
                </th>
                <th>年级</th>
                <th>学院</th>
                <th>专业</th>
                <th>班级</th>
                <th>
                    <div class="ui search">
                        <div class="ui icon input">
                            <input class="prompt" placeholder="搜索" type="text" v-model="keyword"
                                   @keyup.enter="query()">
                            <i class="search link icon" @click="query()"></i>
                        </div>
                    </div>
                </th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>1</td>
                <td>2016</td>
                <td>仁济学院</td>
                <td>护理专业</td>
                <td>3班</td>
                <td>
                    <a href="javascript:void(0);" title="修改">
                        <i class="large write square icon"></i>
                    </a>
                    <a href="javascript:void(0);" title="删除">
                        <i class="large trash icon"></i>
                    </a>
                </td>
            </tr>
            </tbody>
            <tfoot>
            <tr>
                <th colspan="6">
                    <Pagination :conf="conf"></Pagination>
                </th>
            </tr>
            </tfoot>
        </table>
        <div class="ui hidden divider"></div>
    </div>
</template>

<script>
    import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'
    import '../../../../css/style.css'
    import Pagination from '../../util/Pagination.vue'

    let self = null;
    // 不知道为什么访问不到 this.$http 对象（但可以访问 window.Vue.http 对象），不得不出此下策。
    // 在 vm.created() 中将 this 保存至 self 中

    const vm = {
        data() {
            return {
                conf: {
                    currentPage: 1,
                    totalItems: 0,
                    itemsPerPage: 10,
                    refreshCount: 0,
                    uid: null,
                    async onChange(owner) {
                        if (this.uid === owner._uid) {
                            try {
                                let data = await dao.query_entities(
                                    this.currentPage,
                                    this.itemsPerPage,
                                    self.keyword);
                                this.totalItems = data.count;
                                self.dataList = data.data;
                            }
                            catch (err) {
                                console.error(err);
                                self.showErrorDialog({
                                    title: '错误',
                                    message: '数据加载失败，请检查网络情况。',
                                });
                            }
                        }
                    }
                },
                keyword: '',
                dataList: [],
                removeConfirmParams: {
                    show: false,
                    entity: {},
                },
                messageDialogParams: {
                    show: false,
                    title: '',
                    message: '',
                }
            };
        },
        created() {
            self = this;
        },
        mounted() {
        },
        components: {
            Pagination,
        }
    };
    export default vm;
</script>

<style scoped>

</style>