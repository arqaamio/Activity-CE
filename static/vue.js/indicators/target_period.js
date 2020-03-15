Vue.use(VeeValidate);
Vue.component('modal', {
  template: '#modal-template'
});

new Vue({
    delimiters: ['[[', ']]'],
	el: '#indicators_list',
	data: {
        overall_target: '',
        indicator_id: '',
        baseline: '',
        rationale: '',
        target_frequency: '',
        number_of_target_periods: '1',
        target_frequency_start: '',
        showModal: false,
        showDeleteModal: false,
        modalHeader: "Add Target Period",
        isEdit: '',
        currentPeriod: null,
        itemToDelete: null,
        show: false,
        showTable: false,
        disabledClass: false,
        targets: [],
        sum: 0,
        target_value: [0, ],
        frequencies: [{"id": "3", "text":"Annual"},
                      {"id": "4", "text":"Semi-annual"},
                      {"id": "5", "text":"Tri-annual"},
                      {"id": "6", "text":"Quarterly"},
                      {"id": "7", "text":"Monthly"}],       
    },
    methods: {
        makeRequest(method, url, data = null) {
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios.defaults.xsrfCookieName = 'csrftoken';
            return axios({method, url, data});
        },

        updateSum: function(){
            this.sum = 0
            this.target_value.forEach(value => {
                this.sum += parseInt(value)
            });
            
        },

        addPeriodTargets: function() {
            if (this.number_of_target_periods < 1) {
                return;
              }

            const periodStarts = moment(this.target_frequency_start).startOf("month");


            this.frequencies.forEach(frequency => {
                if (frequency.id === this.target_frequency){
                    switch (frequency.id) {
                        case "3":
                          this.generateYearlyTargets(periodStarts);
                          break;
                        case "4":
                          this.generateSemiAnnualTargets(periodStarts);
                          break;
                        case "5":
                          this.generateTriAnnualTargets(periodStarts);
                          break;
                        case "6":
                          this.generateQuarterlyTargets(periodStarts);
                          break;
                        case "7":
                          this.generateMonthlyTargets(periodStarts);
                          break;
                
                        default:
                          break;
                    }

                }
            })

            this.showTable = true
            this.disabledClass = true

            
        },

        removeTargetPeriods: function(){
            this.targets= [],
            this.target_value= [0, ]
            this.sum= 0
            this.show=false
            this.showTable = false
            this.disabledClass = false
            this.target_frequency_start= ''

        },

        showFields: function(){
            this.show = true
        },

        generateYearlyTargets: function(periodStart){
            for (let i = 1; i <= this.number_of_target_periods; i++) {
                const period = `Year ${i}`
                const id = `${i}`
                let periodEnds = moment(periodStart);
                let start_date = moment(periodStart)
                            .startOf("month")
                            .format("MMM DD, YYYY");
                let end_date = moment(periodEnds)
                            .add(11, "months")
                            .endOf("month")
                            .format("MMM DD, YYYY");


                this.targets = [...this.targets, { id, start_date, end_date, period}];

                periodStart = moment(periodEnds).add(12, "months");
            }

        },

        generateSemiAnnualTargets: function(periodStart){
            for (let i = 1; i <= this.number_of_target_periods; i++) {
                const period = `SemiAnnual ${i}`
                const id = `${i}`
                let periodEnds = moment(periodStart);
                let start_date = moment(periodStart)
                            .startOf("month")
                            .format("MMM DD, YYYY");
                let end_date = moment(periodEnds)
                            .add(5, "months")
                            .endOf("month")
                            .format("MMM DD, YYYY");

                this.targets = [...this.targets, { id, start_date, end_date, period}];

                periodStart = moment(periodEnds).add(6, "months");
            }

        },

        generateTriAnnualTargets: function(periodStart){
            for (let i = 1; i <= this.number_of_target_periods; i++) {
                const period = `Triannual ${i}`
                const id = `${i}`
                let periodEnds = moment(periodStart);
                let start_date = moment(periodStart)
                            .startOf("month")
                            .format("MMM DD, YYYY");
                let end_date = moment(periodEnds)
                            .add(3, "months")
                            .endOf("month")
                            .format("MMM DD, YYYY");


                this.targets = [...this.targets, { id, start_date, end_date, period}];

                periodStart = moment(periodEnds).add(4, "months");
            }

        },

        generateQuarterlyTargets: function(periodStart){
            for (let i = 1; i <= this.number_of_target_periods; i++) {
                const period = `Quarter ${i}`
                const id = `${i}`
                let periodEnds = moment(periodStart)
                let start_date = moment(periodStart)
                            .startOf("month")
                            .format("MMM DD, YYYY");
                let end_date = moment(periodEnds)
                            .add(2, "months")
                            .endOf("month")
                            .format("MMM DD, YYYY");


                this.targets = [...this.targets, { id, start_date, end_date, period}];

                periodStart = moment(periodEnds).add(3, "months");
            }
        },

        generateMonthlyTargets: function(periodStart){
            for (let i = 1; i <= this.number_of_target_periods; i++) {
                const period = `Month ${i}`
                const id = `${i}`
                let periodEnds = moment(periodStart)
                let start_date = moment(periodStart)
                            .startOf("month")
                            .format("MMM DD, YYYY");
                let end_date = moment(periodEnds)
                            .add("months")
                            .endOf("month")
                            .format("MMM DD, YYYY");

                this.targets = [...this.targets, { id, start_date, end_date, period}];

                periodStart = moment(periodEnds).add(1, "months");
            } 
        },


        toggleTargetModal: function(indicator_id) {
            this.showModal = !this.showModal
            this.indicator_id = indicator_id
            this.overall_target = ''
            this.baseline= 0
            this.rationale= ''
            this.target_frequency= ''
            this.number_of_target_periods= '1'
            this.target_frequency_start= ''
            this.targets= [],
            this.target_value= [0, ]
            this.sum= 0
            this.show=false
            this.showTable = false
            this.disabledClass = false

        },

        processForm: function() {
            this.$validator.validateAll().then(target => {
                if (target) {
                    if (this.targets.length > 0){
                        if (this.sum === parseInt(this.overall_target)){
                            this.postTarget()
                        }else{
                            toastr.error('The sum of target values must be equal to overall target');
                        }
                    }else{
                        toastr.error('Please add period targets');
                    }
                }
            });
        },

        async postTarget() {
            this.target_value.forEach((item, index) => {
                this.targets.forEach((target =>{
                    if (index === parseInt(target.id)){
                        target["target"] = item
                    }
                }))
            })
            const id = this.indicator_id
            this.targets = this.targets.map(function (obj) {
                obj['indicator_id'] = obj['id'];
                obj['start_date'] = moment(obj['start_date']).format("YYYY-MM-DD")
                obj['end_date'] = moment(obj['end_date']).format("YYYY-MM-DD")
                delete obj['id'];
                obj['indicator_id'] = id
                return obj;
            });
            const data = {
                indicator_id : id,
                indicator_LOP: this.overall_target,
                indicator_baseline: this.baseline,
                rationale : this.rationale,
                periodic_targets: this.targets
            }

            try {
                const response = await this.makeRequest(
                    'POST',
                    `/indicators/periodic_target/`,
                    {data}
                  );

                if (response){
                    this.toggleTargetModal();
                    toastr.success('Target periods were saved successfully');
                    this.$validator.reset();
                }
            } catch (error) {
                toastr.error('There was a problems saving your data.');
            }

        },

    },
    computed: {
        /**
        * Check if frequency form is valid
        */
        isFormValid() {
            return true;
        },
    },
});