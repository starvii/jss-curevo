<template>
    <DialogFrame :show="params['show']" :closeFunc="doCancel">
        <span slot="header">{{ params['title'] }}</span>
        <span>{{ params['message'] }}</span>
        <div slot="actions">
            <div class="ui red cancel inverted button" @click="doConfirm">
                <i class="remove icon"></i>
                确认
            </div>
            <div class="ui green ok inverted button" @click="doCancel">
                <i class="checkmark icon"></i>
                取消
            </div>
        </div>
    </DialogFrame>
</template>

<script>
    import DialogFrame from './DialogFrame.vue'

    const vm = {
        props: {
            params: {
                type: Object, // {show, title, message, confirmFunc}
                require: true,
            },
        },
        components: {
            DialogFrame,
        },
        methods: {
            doCancel() {
                this.params['show'] = false;
            },
            doConfirm() {
                // do something
                this.params['confirmFunc']();
                this.params['show'] = false;
            },
        },
    };

    export default vm;
</script>