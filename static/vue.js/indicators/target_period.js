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
        disabledClass: false,
        frequencies: [],
        targets: [],
        sum: 0,
        target_value: [0, ],
    },
    beforeMount: function() {
		this.makeRequest('GET', '/indicators/data_collection_frequency/')
			.then(response => {
				if (response.data) {
                    if (this.frequencies.length === 0){
                        response.data.forEach(frequency =>{
                            this.frequencies.push({"id": frequency.id, "text": frequency.frequency})
                        })   
                    }
                }		
			})
			.catch(e => {
				toastr.error('There was a problem loading frequencies from the database');
				this.frequencies = [];
			});
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
                    switch (frequency.text) {
                        case "Annual":
                          this.generateYearlyTargets(periodStarts);
                          break;
                        case "Semi-annual":
                          this.generateSemiAnnualTargets(periodStarts);
                          break;
                        case "Tri-annual":
                          this.generateTriAnnualTargets(periodStarts);
                          break;
                        case "Quarterly":
                          this.generateQuarterlyTargets(periodStarts);
                          break;
                        case "Monthly":
                          this.generateMonthlyTargets(periodStarts);
                          break;
                
                        default:
                          break;
                    }

                }
            })

            
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
                let start = moment(periodStart)
                            .startOf("month")
                            .format("MMM DD, YYYY");
                let end = moment(periodEnds)
                            .add(3, "months")
                            .endOf("month")
                            .format("MMM DD, YYYY");


                this.targets = [...this.targets, { id, start, end, period}];

                periodStart = moment(periodEnds).add(4, "months");
            }

        },

        generateQuarterlyTargets: function(periodStart){
            for (let i = 1; i <= this.number_of_target_periods; i++) {
                const period = `Quarter ${i}`
                const id = `${i}`
                let periodEnds = moment(periodStart)
                                 .subtract(1, "months")
                                 .add(1, "quarters");
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


        toggleTargetModal: function(indicator_id, item = null) {
            this.showModal = !this.showModal
            this.indicator_id = indicator_id 
        },

        processForm: function() {
            this.$validator.validateAll().then(target => {
                if (target) {
                  if (this.currentPeriod && this.currentPeriod.id) {
                    this.updateTarget();
                  } else {
                    this.postTarget()
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
            console.log(this.targets)
            const id = this.indicator_id
            this.targets = this.targets.map(function (obj) {
                obj['indicator_id'] = obj['id'];
                obj['start_date'] = moment(obj['start_date']).format("YYYY-MM-DD")
                obj['end_date'] = moment(obj['end_date']).format("YYYY-MM-DD")
                delete obj['id'];
                obj['indicator_id'] = id
                return obj;
            });
            console.log(this.targets)
            const data = {
                indicator_id : id,
                indicator_LOP: this.overall_target,
                indicator_baseline: this.baseline,
                rationale : this.rationale,
                periodic_targets: this.targets
            }
            console.log(data)

            try {
                const response = await this.makeRequest(
                    'POST',
                    `/indicators/periodic_target/`,
                    {data}
                  );

                if (response){
                    console.log(response)
                }
            } catch (error) {
                alert('error')
            }

        },

        async updateTarget() {

        },

        async deleteObjective(id) {

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