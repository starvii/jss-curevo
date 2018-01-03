<template>
    <div class="ui form">
        <div class="two fields">
            <div class="field">
                <label>年级</label>
                <input placeholder="年级" type="text" v-model="entity['Grade']">
            </div>
            <div class="field">
                <label>学院</label>
                <input placeholder="学院" type="text" v-model="entity['BelongToCollege']">
            </div>
        </div>
        <div class="three fields">
            <div class="field">
                <label>专业</label>
                <input placeholder="专业" type="text" v-model="entity['Dept']">
            </div>
            <div class="field">
                <label>班级</label>
                <input placeholder="班级" type="text" v-model="entity['Name']">
            </div>
            <div class="field">
                <label>人数</label>
                <input placeholder="人数" type="text" v-model="entity['StudentCount']">
            </div>
        </div>
        <div class="field">
            <label>备注</label>
            <textarea rows="3" style="resize: none;" placeholder="备注"
                      v-model="entity['Comment']"></textarea>
        </div>
        <div class="ui hidden divider"></div>
    </div>
</template>

<script>
    const vm = {
        props: {
            entity: {
                type: Object,
                require: true,
            }
        },
    };
    export default vm;
</script>