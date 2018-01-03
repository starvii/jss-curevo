<template>
    <div class="container">
        <div v-for="(item, index) in dataList">
            <h1 v-text="index + 1"></h1>
            <AddForm :entity="item"></AddForm>
        </div>
        <div class="ui icon buttons orange">
            <div class="ui button" title="新建" @click="addComponent()">
                <i class="plus icon"></i>
            </div>
        </div>
        <div class="ui hidden divider"></div>
    </div>
</template>

<script>
    import AddForm from './AddForm.vue'

    const vm = {
        data() {
            return {
                dataList: [{}],

            };
        },
        components: {
            AddForm
        },
        methods: {
            addComponent() {
                this.dataList.push({});
            },
        },
    };
    export default vm;
</script>