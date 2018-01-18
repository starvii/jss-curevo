<template>
    <v-app>
        <v-content>
            <v-container fluid>
                <v-toolbar dark color="primary">
                    <v-icon>today</v-icon>
                    <v-toolbar-title class="white--text">排课辅助工具</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn flat color="white" class="white--text" @click.native.stop="helpDlgOpen = true">
                        <v-icon dark>help</v-icon>
                        日历格式说明
                    </v-btn>
                    <v-btn flat color="white" class="white--text" @click="setPerWeek()">
                        <v-icon dark>date_range</v-icon>
                        设置每周课程数量
                    </v-btn>
                    <v-btn flat color="white" class="white--text" @click.native.stop="resultDlgOpen = true">
                        <v-icon dark>view_comfy</v-icon>
                        显示课表模板
                    </v-btn>
                    <v-btn flat color="white" class="white--text" @click="genCsv()">
                        <v-icon dark>get_app</v-icon>
                        下载课表模板
                    </v-btn>
                </v-toolbar>
                <v-layout row>
                    <v-flex xl1>
                        <v-subheader>教学日历</v-subheader>
                    </v-flex>
                    <v-flex xl11>
                        <v-text-field
                                label="教学日历"
                                multi-line
                                v-model="calender"
                                :rules="[() => !!calender && calender.trim().length > 0 || '必须填写']"
                        ></v-text-field>
                    </v-flex>
                </v-layout>
                <v-layout row>
                    <v-flex xl1>
                        <v-subheader>课程名称</v-subheader>
                    </v-flex>
                    <v-flex xl11>
                        <v-text-field
                                label="课程名称"
                                v-model="lessonName"
                                :rules="[() => !!lessonName && lessonName.trim().length > 0 || '必须填写']"
                        ></v-text-field>
                    </v-flex>
                </v-layout>
                <v-layout row>
                    <v-flex xl1>
                        <v-subheader>教学班级</v-subheader>
                    </v-flex>
                    <v-flex xl11>
                        <v-text-field
                                label="教学班级"
                                v-model="className"
                                :rules="[() => !!className && className.trim().length > 0 || '必须填写']"
                        ></v-text-field>
                    </v-flex>
                </v-layout>
                <v-layout row>
                    <v-flex xl1>
                        <v-subheader>
                            每周课程
                        </v-subheader>
                    </v-flex>
                    <v-flex xl11>
                        <v-text-field
                                label="每周课程数"
                                v-model="perWeek"
                                @keyup.enter="setPerWeek()"
                                :rules="[() => !!perWeek && perWeek > 0 && perWeek <= 10 || '必须为整数且范围在1-10之内']"
                                mask="##"
                        ></v-text-field>
                    </v-flex>
                </v-layout>
                <v-layout row v-for="item in weekLessons" :key="item">
                    <v-flex xl3>&nbsp;</v-flex>
                    <v-flex xl3>
                        <v-select
                                v-bind:items="weekdays"
                                label="星期"
                                v-model="item.weekday"
                        ></v-select>
                    </v-flex>
                    <v-flex xl3>
                        <v-select
                                v-bind:items="lessonTime"
                                label="节次"
                                v-model="item.time"
                        ></v-select>
                    </v-flex>
                    <v-flex xl3>
                        &nbsp;
                    </v-flex>
                </v-layout>
                <v-footer class="pa-3">
                    <v-spacer></v-spacer>
                    <div>WHATEVER © {{ new Date().getFullYear() }}</div>
                </v-footer>
            </v-container>
            <v-dialog v-model="helpDlgOpen" fullscreen transition="dialog-bottom-transition" :overlay=false>
                <v-card>
                    <h1>教学日历格式说明</h1>
                    <v-card-text>
                        <v-card-title class="headline">教学日历基本格式</v-card-title>
                        <v-flex offset-xl1>
                            <p>
                                {学期范围} - {假期} + {调休}
                            </p>
                        </v-flex>
                        <v-card-title class="headline">日期格式</v-card-title>
                        <v-flex offset-xl1>
                            <p>YYYYMMDD（例如20180123）</p>
                            <p>可用“YYYYMMDD-YYYYMMDD”表示日期范围</p>
                            <p>可用“SAT”、“SUN”表示周六、周日</p>
                            <p>调休中使用“YYYYMMDD(YYYYMMDD)”表示替换</p>
                            <p>例如“20180505(20180429)”表示20180505补上20180429的课程</p>
                        </v-flex>
                        <v-card-title class="headline">一个栗子</v-card-title>
                        <v-flex offset-xl1>
                            <p>{20160912 - 20170129}<br/>
                                -{SAT, SUN, 20160915 - 20160916, 20170102}<br/>
                                +{20160918(20160916), 20161008(20161006)}</p>
                        </v-flex>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="green darken-1" outline flat="flat" @click.native="helpDlgOpen = false">知道了
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-dialog v-model="resultDlgOpen" fullscreen transition="dialog-bottom-transition" :overlay=false>
                <v-card>
                    <v-card-title class="headline">课表模板</v-card-title>
                    <v-card-text>
                        <p>请将以下内容保存至扩展名为csv的文本文件中，即可使用Excel编辑</p>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="green darken-1" outline flat="flat" @click.native="resultDlgOpen = false">返回
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-content>
    </v-app>
</template>

<script>
    const vm = {
        data() {
            return {
                calender: '',
                lessonName: '',
                className: '',
                perWeek: 1,
                weekdays: [
                    {text: '一', value: 'MON'},
                    {text: '二', value: 'TUE'},
                    {text: '三', value: 'WED'},
                    {text: '四', value: 'THU'},
                    {text: '五', value: 'FRI'},
                    {text: '六', value: 'SAT'},
                    {text: '日', value: 'SUN'},
                ],
                lessonTime: [
                    {text: '1-2'},
                    {text: '3-4'},
                    {text: '3-5'},
                    {text: '6-7'},
                    {text: '6-8'},
                    {text: '6-9'},
                    {text: '8-9'},
                    {text: '10-11'},
                    {text: '10-12'},
                ],
                weekLessons: [],
                helpDlgOpen: false,
                resultDlgOpen: false,
            }
        },
        mounted() {
            this.setPerWeek();
        },
        methods: {
            setPerWeek() {
                if (this.perWeek <= 0 || this.perWeek > 10) {
                    return;
                }
                this.weekLessons = [];
                for (let i = 0; i < this.perWeek; i++) {
                    this.weekLessons.push(
                        {id: i, 'weekday': '', 'time': ''}
                    );
                }
            },
            genCsv() {
                let data = {
                    calender: this.calender,
                    lessonName: this.lessonName,
                    className: this.className,
                    weekLessons: this.weekLessons
                };
                Vue.http.post('api/v1', data).then(
                    response => {

                    },
                    response => {

                    }
                )
            },
        }
    };

    export default vm;

</script>