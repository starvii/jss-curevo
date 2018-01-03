<template>
    <DialogFrame :show="params['show']" :closeFunc="doClose">
        <span slot="header">{{ params['title'] }}</span>
        <i class="red massive warning circle icon"></i>
        <span>{{ params['message'] }}</span>
        <div slot="actions">
            <div class="ui red cancel inverted button" @click="doClose">
                <i class="remove icon"></i>
                关闭
            </div>
        </div>
    </DialogFrame>
</template>

<script>
    import DialogFrame from './DialogFrame.vue'

    const MessageDialog = {
        props: {
            params: {
                type: Object, // {title, message, show}
                require: true,
            },
        },
        components: {
            DialogFrame,
        },
        methods: {
            doClose() {
                this.params.show = false;
            },
        },
    };

    export default MessageDialog;
</script>