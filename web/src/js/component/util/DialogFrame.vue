<template>
    <div class="ui dimmer modals page transition" :class="showState ? 'visible active' : 'hidden'"
         style="display: block !important;" v-if="showState" @click.self="doDimmer()">
        <div :id="pid" class="ui modal transition hidden" :class="showState ? 'visible active' : 'hidden'"
             style="display: block !important;">
            <div class="header">
                <button class="ui right floated icon button basic mini" @click="doClose()">
                    <i class="close icon"></i>
                </button>
                <slot name="header">
                    Dialog Header
                </slot>
            </div>

            <div class="content">
                <slot>
                    Dialog Content
                </slot>
            </div>
            <div class="actions">
                <slot name="actions">
                    Dialog Actions
                </slot>
            </div>
        </div>
    </div>
</template>

<script>
    import hash from 'object-hash';

    const DialogFrame = {
        data() {
            return {
                temp: '',
            };
        },
        props: {
            show: {
                type: Boolean,
            },
            id: {
                type: String,
            },
            closeFunc: {
                type: Function,
                require: true,
            },
            dimmerFunc: {
                type: Function,
            },
        },
        computed: {
            showState() {
                if ('undefined' === typeof(this.show) || (false !== this.show && true !== this.show)) {
                    return false;
                }
                return this.show;
            },
            pid() {
                if (this.temp.length > 0) {
                    return this.temp;
                }
                // 如果父组件没有提供id，则随机生成一个。供jquery居中窗口使用。
                if ('undefined' === typeof(this.id) || this.id.length === 0) {
                    let seed = Math.random();
                    let timestamp = (new Date()).valueOf();
                    this.temp = hash(`${timestamp}${seed}`);
                    return this.temp;
                }
                return this.id;
            },
        },
        updated() {
            let id = `#${this.pid}`;
            let h = parseInt(jQuery(id).height()) / 2;
            jQuery(id).css('margin-top', `-${h}px`);
        },
        methods: {
            doClose() {
                this.closeFunc();
            },
            doDimmer() {
                if ('undefined' !== typeof(this.dimmerFunc)) {
                    this.dimmerFunc();
                }
            },
        },
    };

    export default DialogFrame;
</script>
