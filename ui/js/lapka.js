window.onload = function () {

    var app,
        animalData = {
            name: '',
            age: 0,
            place:'' ,
            description: ''
        },
        baseUrl = window.location.protocol + "//" + window.location.host + "/api/";

    Vue.component('custom-header', {
        template: "<header>I'm a header</header>"
    });

    Vue.component('custom-footer', {
        template: "<footer>I'm a footer</footer>"
    });

    Vue.component('animal-profile', {
        // XXX Other ways: http://stackoverflow.com/q/31633573
        template: '#animal-profile-tmpl',
        data: function () {
            return animalData;
        }
    });

    Vue.component('social-connect', {
        template: '#social-connect-tmpl',
        data: function () {
            return {
                // FIXME Populate connected social accounts
                platforms: [
                    {
                        name: 'facebook',
                        connected: true
                    },
                    {
                        name: 'google',
                        connected: false
                    }
                ]
            };
        },
        methods: {
            // FIXME Implement (dis)connecting socials accounts
            connect: function (e) {
                console.info("Connecting");
            },
            disconnect: function (e) {
                console.info("Disconnecting");
            }
        },
        mounted: function () {
            console.info("Mounted");
            this.platforms[0].connected = false;  // XXX Remove me
        },
        beforeDestroy: function () {
            console.info("beforeDestroy - do clean up");
        }
    });

    Vue.component('profile-settings', {
        template: '#profile-settings-tmpl',
        data: function () {
            // FIXME Populate user preferences
            return {
                species: [],
                sex: [],
                cities: []
            };
        },
        methods: {
            onSubmit: function (e) {
                console.info('Submitted data');
            },
            fetchData: function () {
                console.log('Can I haz data pleaz');
            }
        },
        mounted: function () {
            this.fetchData();
        }
    });

    animalData.name = 'Doggy';
    animalData.age = 15;
    animalData.place = 'City';
    animalData.description = 'Naughty dog!';

    app = new Vue({
        el: '#app',
        data: {
            message: 'Your profile',
        }
    });
};
