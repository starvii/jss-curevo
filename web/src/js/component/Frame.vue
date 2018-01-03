<!-- 遗传算法整个设置流程 -->
<template>
    <div class="container">
        <TopMenu></TopMenu>
        <div id="wrapper">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'
    import TopMenu from './TopMenu.vue'

    const vm = {
        mounted() {
            jQuery('.ui.dropdown').dropdown();
            setTimeout(() => {
                jQuery('.ui.dropdown').dropdown();
            }, 500);
            setInterval(() => {
                this.resize();
            }, 500);
        },
        components: {
            TopMenu,
        },
        computed: {
            ...mapGetters(['frame$isOutSize']),
        },
        methods: {
            ...mapMutations(['frame$setOutSize']),
            resize() {
                let winInnerHeight = window.innerHeight;
                let menuHeight = jQuery('#topMenu').height();
                let routerViewHeight = jQuery('#wrapper').height();
                let outSize = menuHeight + routerViewHeight > winInnerHeight;
                if (this.frame$isOutSize !== outSize) {
                    this.frame$setOutSize({
                        outSize: outSize,
                    });
                }
            },
        },
    };

    export default vm;
</script>