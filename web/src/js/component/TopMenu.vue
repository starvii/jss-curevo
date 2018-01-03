<template>
    <div id="topMenu" class="ui massive top menu">
        <router-link to="/" class="header item">
            <i class="huge loading world icon"></i>CUREVO
        </router-link>
        <router-link to="/teacher/" class="item">教师管理</router-link>
        <div class="ui dropdown item">
            课程管理
            <i class="dropdown icon"></i>
            <div class="menu">
                <router-link to="/course/" class="item">课程章节</router-link>
                <router-link to="/course/dependency/" class="item">章节依赖</router-link>
            </div>
        </div>
        <div class="ui dropdown item">
            班级管理
            <i class="dropdown icon"></i>
            <div class="menu">
                <router-link to="/class/natural/" class="item">行政班</router-link>
                <router-link to="/class/teaching/" class="item">教学班</router-link>
            </div>
        </div>
        <div class="ui right item dropdown">
            <i class="big user icon"></i>
            超级管理员
            <i class="dropdown icon"></i>
            <div class="menu">
                <router-link to="/profile/" class="item">个人资料</router-link>
                <router-link to="/password/" class="item">修改密码</router-link>
                <router-link to="/logout/" class="item">注销退出</router-link>
            </div>
        </div>
    </div>
</template>

<script>
    const vm = {
    };

    export default vm;
</script>

<style scoped>
    * {
        margin: 0;
        padding: 0;
    }

    #topMenu {
        height: 100px;
        border-radius: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
</style>