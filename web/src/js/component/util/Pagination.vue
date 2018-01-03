<template>
    <div>
        <div class="ui form" v-if="conf.totalItems > 0">
            <div class="inline fields margin0">
                <div class="field">
                    <div class="ui pagination menu">
                        <a class="icon item" :class="{'disabled': conf.currentPage === 1}" @click="prevPage()">
                            <i class="left chevron icon"></i>
                        </a>
                        <a class="item" v-for="item in pageList"
                           :class="[item === '...' ? 'disabled' : '', {'active': item === conf.currentPage}]"
                           @click="changeCurrentPage(item)">
                            <span v-text="item"></span>
                        </a>
                        <a class="icon item" :class="{'disabled': conf.currentPage === conf.numberOfPages}"
                           @click="nextPage()">
                            <i class="right chevron icon"></i>
                        </a>
                    </div>
                </div>
                <div class="field">
                    <label>第</label>
                    <input type="text" v-model="jumpPageNum" style="width: 75px !important;"
                           @keyup.enter="jumpToPage()"/>
                    <label>页</label>
                    <label>每页</label>
                    <select class="ui search" v-model="conf.itemsPerPage" style="width: 75px !important;">
                        <option v-for="option in conf.perPageOptions">{{option}}</option>
                    </select>
                    <label>条</label>
                    <label>共<strong v-text="conf.totalItems"></strong>条</label>
                </div>
            </div>
        </div>
        <div class="ui pagination menu" v-if="conf.totalItems <= 0">
            <a class="icon item">
                <i class="left chevron icon"></i>
            </a>
            <a class="item">暂无数据</a>
            <a class="icon item">
                <i class="right chevron icon"></i>
            </a>
        </div>
    </div>
</template>

<script>
    import '../../../css/style.css'

    // 默认分页长度
    const defaultPagesLength = 9;

    // 默认分页选项可调整每页显示的条数
    const defaultPerPageOptions = [10, 15, 30, 50, 100];

    // 默认每页的个数
    const defaultPerPage = 10;

    const Pagination = {
        replace: true,
        data() {
            return {
                pageList: [],
                jumpPageNum: '',
                lastPageValue: '',
            };
        },
        props: {
            /**
             * conf {
             *     currentPage: 1,                          当前页
             *     totalItems: 8000,                        条目总数
             *     itemsPerPage: 15,                        每页显示条目数
             *     pagesLength: 15,                         分页器上显示元素个数
             *     perPageOptions: [10, 20, 30, 40, 50],    每页显示条目数选项
             *     rememberPerPage: 'perPageItems',         不详
             *     onChange: function(){},                  翻页时触发方法
             *     refreshCount: 0,                         用于控制刷新。由于直接调用 onChange 常常会导致请求两次
             *     uid: null,                               一个页面上如果有多个相同分页控件，仅响应第一个请求
             * }
             * */
            conf: {
                type: Object,
                required: true,
            },
        },
        created() {
            if (!this.conf.uid) {
                this.conf.uid = this._uid;
            }
        },
        mounted() {
            // 获取分页长度
            if (this.conf.pagesLength) {
                // 判断一下分页长度
                this.conf.pagesLength = parseInt(this.conf.pagesLength, 10);
                if (!this.conf.pagesLength) {
                    this.conf.pagesLength = defaultPagesLength;
                }

                // 分页长度必须为奇数，如果传偶数时，自动处理
                if (this.conf.pagesLength % 2 === 0) {
                    this.conf.pagesLength += 1;
                }
            } else {
                this.conf.pagesLength = defaultPagesLength;
            }

            // 分页选项可调整每页显示的条数
            if (!this.conf.perPageOptions) {
                this.conf.perPageOptions = defaultPerPageOptions;
            }

            // 使用 vue api 的 $watch 自动监测状态变化
            this.$watch(this.getWatchState, this.watchFunc);
            // 使用了 {immediate: true} 会立即响应，不需要再调用一次。
            this.getPagination();
        },
        methods: {
            // pageList数组
            getPagination() {
                if (this.conf.currentPage) {
                    this.conf.currentPage = parseInt(this.conf.currentPage, 10);
                }

                if (!this.conf.currentPage) {
                    this.conf.currentPage = 1;
                }

                // conf.totalItems
                if (this.conf.totalItems) {
                    this.conf.totalItems = parseInt(this.conf.totalItems, 10);
                }
                if (!this.conf.totalItems) {
                    this.conf.totalItems = 0;
                    return;
                }

                // conf.itemsPerPage
                if (this.conf.itemsPerPage) {
                    this.conf.itemsPerPage = parseInt(this.conf.itemsPerPage, 10);
                }
                if (!this.conf.itemsPerPage) {
                    this.conf.itemsPerPage = defaultPerPage;
                }

                // numberOfPages
                this.conf.numberOfPages = Math.ceil(this.conf.totalItems / this.conf.itemsPerPage);

                // 如果分页总数>0，并且当前页大于分页总数
                if (this.conf.numberOfPages > 0 && this.conf.currentPage > this.conf.numberOfPages) {
                    this.conf.currentPage = this.conf.numberOfPages;
                }

                // 如果itemsPerPage在不在perPageOptions数组中，就把itemsPerPage加入这个数组中
                let perPageOptionsLength = this.conf.perPageOptions.length; // TODO: 有待研究

                // 定义状态
                let perPageOptionsStatus;
                for (let i = 0; i < perPageOptionsLength; i++) {
                    if (this.conf.perPageOptions[i] === this.conf.itemsPerPage) {
                        perPageOptionsStatus = true;
                    }
                }

                // 如果itemsPerPage在不在perPageOptions数组中，就把itemsPerPage加入这个数组中
                if (!perPageOptionsStatus) {
                    this.conf.perPageOptions.push(this.conf.itemsPerPage);
                }

                // 对选项进行sort
                this.conf.perPageOptions.sort((a, b) => {
                    return a - b
                });

                // 页码相关
                this.pageList = [];
                if (this.conf.numberOfPages <= this.conf.pagesLength) {
                    // 判断总页数如果小于等于分页的长度，若小于则直接显示
                    for (let i = 1; i <= this.conf.numberOfPages; i++) {
                        this.pageList.push(i);
                    }
                } else {
                    // 总页数大于分页长度（此时分为三种情况：1.左边没有...2.右边没有...3.左右都有...）
                    // 计算中心偏移量
                    let offset = (this.conf.pagesLength - 1) / 2;
                    if (this.conf.currentPage <= offset) {
                        // 左边没有...
                        for (let i = 1; i <= offset + 1; i++) {
                            this.pageList.push(i);
                        }
                        this.pageList.push('...');
                        this.pageList.push(this.conf.numberOfPages);
                    } else if (this.conf.currentPage > this.conf.numberOfPages - offset) {
                        this.pageList.push(1);
                        this.pageList.push('...');
                        for (let i = offset + 1; i >= 1; i--) {
                            this.pageList.push(this.conf.numberOfPages - i);
                        }
                        this.pageList.push(this.conf.numberOfPages);
                    } else {
                        // 最后一种情况，两边都有...
                        this.pageList.push(1);
                        this.pageList.push('...');

                        for (let i = Math.ceil(offset / 2); i >= 1; i--) {
                            this.pageList.push(this.conf.currentPage - i);
                        }
                        this.pageList.push(this.conf.currentPage);
                        for (let i = 1; i <= offset / 2; i++) {
                            this.pageList.push(this.conf.currentPage + i);
                        }

                        this.pageList.push('...');
                        this.pageList.push(this.conf.numberOfPages);
                    }
                }
            },

            // 前一页
            prevPage() {
                if (this.conf.currentPage > 1) {
                    this.conf.currentPage -= 1;
                }
                this.getPagination();
            },

            // 下一页
            nextPage() {
                if (this.conf.currentPage < this.conf.numberOfPages) {
                    this.conf.currentPage += 1;
                }
                this.getPagination();
            },

            // 变更当前页
            changeCurrentPage(item) {
                if (item === '...') {
                } else {
                    this.conf.currentPage = item;
                    this.getPagination();
                }
            },

            // 修改每页展示的条数
            changeItemsPerPage() {
                this.conf.currentPage = 1;
                this.getPagination();
            },

            // 跳转页
            jumpToPage() {
                let num = this.jumpPageNum;
                if (num.match(/\d+/)) {
                    num = parseInt(num, 10);
                    if (num && num !== this.conf.currentPage) {
                        if (num > this.conf.numberOfPages) {
                            num = this.conf.numberOfPages;
                        }

                        // 跳转
                        this.conf.currentPage = num;
                        this.getPagination();
                        this.jumpPageNum = '';
                    }
                }
            },
            getWatchState() {
                if (!this.conf.totalItems) {
                    this.conf.totalItems = 0;
                }
                return `${this.conf.totalItems},${this.conf.currentPage},${this.conf.itemsPerPage},${this.conf.refreshCount}`;
            },
            changeFunc() {
                if (this.conf.onChange) {
                    this.conf.onChange(this);
                }
            },
            watchFunc(newVal, oldVal) {
//                if (!newVal || newVal === oldVal) { // 原语句是这样写的，奇怪，不知道为什么
                if (newVal !== oldVal) {
                    this.changeFunc();
                }
                this.getPagination();
            },
        },
    };

    export default Pagination;
</script>
