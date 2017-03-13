window.onload = function () {

    var app,
        animalData = {
            id: '',
            name: '',
            age: 0,
            place:'' ,
            description: '',
            photos: []
        },
        baseUrl = "/",
        userId = 'user-id';  // TODO Set to real id

    Vue.component('custom-header', {
        template: "<header>I'm a header</header>"
    });

    Vue.component('custom-footer', {
        template: "<footer>I'm a footer</footer>"
    });

    function httpError(url) {
        return function (error) {
            console.warn("Could not fetch data from", url, ":", error);
        };
    }

    Vue.component('animal-profile', {
        // XXX Other ways: http://stackoverflow.com/q/31633573
        template: '#animal-profile-tmpl',
        data: function () {
            return {
                animal: animalData,
                next: null,
                matching: [],  // list of animals ids
                // lru: {}
            };
        },
        methods: {
            _get: function (url, success) {
                var url = baseUrl + url + '/';
                axios.get(url)
                  .then(success)
                  .catch(httpError(url));
            },
            _fetchMatching: function (success) {
                var $this = this;
                this._get('animal/matching/' + userId, function (resp) {
                    $this.matching = resp.data;
                    if (typeof success === 'function') {
                        success(resp)
                    }
                });

            },
            like: function (uid, e) {  // TODO Implement
                window.alert("Liked " + uid);
            },
            seeNext: function (curr_uid) {
                var $this = this;
                function switchAnimals() {
                    $this.animal = $this.next;
                    $this.next = null;
                }

                if (curr_uid) {
                    axios.post(baseUrl + 'animal/skip/' + userId + '/');
                }

                if (this.next === null) {
                    this.fetchNext(switchAnimals);
                } else {
                    switchAnimals();
                }
            },
            fetchNext: function (success) {
                if (this.next !== null) {
                    return;
                }

                var $this = this,
                    uid = this.matching.shift();

                if (uid === undefined) {
                    return;
                }
                this._get('animal/' + uid, function(resp) {
                    $this.next = resp.data;
                    if (typeof success === 'function') {
                        success(resp)
                    }
                });
            }
        },
        mounted: function () {
            var $this = this;
            this._fetchMatching(function () {
                $this.seeNext();
            });
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
        el: '#animal-app',
        data: {
            message: 'Your profile',
        }
    });
};
