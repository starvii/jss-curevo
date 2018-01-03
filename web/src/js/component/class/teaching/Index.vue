<template>
    <div class="container">
        <table class="ui celled table">
            <thead>
            <tr v-if="false">
                <th colspan="6">
                    <!--Pagination-->
                </th>
            </tr>
            <tr>
                <th colspan="6">
                    <div class="ui grid">
                        <div class="five wide column">
                            <div class="ui icon buttons orange">
                                <div class="ui button" title="新建">
                                    <i class="plus icon"></i>
                                </div>
                            </div>
                        </div>
                        <div class="six wide column"></div>
                        <div class="five wide column">
                            <div class="ui form">
                                <div class="ui action input">
                                    <input placeholder="搜索..." type="text">
                                    <div class="ui icon button green" title="搜索"><i class="search icon"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </th>
            </tr>
            <tr>
                <th>序号</th>
                <th>年级</th>
                <th>学院</th>
                <th>专业</th>
                <th>班级</th>
                <th>操作</th>
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
                        <i class="write square icon"></i>
                    </a>
                    <a href="javascript:void(0);" title="删除">
                        <i class="trash icon"></i>
                    </a>
                </td>
            </tr>
            </tbody>
            <tfoot>
            <tr>
                <th colspan="6">
                    分页器
                </th>
            </tr>
            </tfoot>
        </table>
        <div class="ui hidden divider"></div>
    </div>
</template>

<script>
    let self = null;
    // 不知道为什么访问不到 this.$http 对象（但可以访问 window.Vue.http 对象），不得不出此下策。
    // 在 vm.created() 中将 this 保存至 self 中

    const NaturalIndex = {
        data() {
            return {

            };
        },
        created() {
            self = this;
        },
        mounted() {
        },
    };
    export default NaturalIndex;
</script>