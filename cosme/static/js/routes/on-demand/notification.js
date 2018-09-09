!function (t) {
    var n = {};

    function e(i) {
        if (n[i]) return n[i].exports;
        var r = n[i] = {i: i, l: !1, exports: {}};
        return t[i].call(r.exports, r, r.exports, e), r.l = !0, r.exports
    }

    e.m = t, e.c = n, e.d = function (t, n, i) {
        e.o(t, n) || Object.defineProperty(t, n, {
            configurable: !1,
            enumerable: !0,
            get: i
        })
    }, e.r = function (t) {
        Object.defineProperty(t, "__esModule", {value: !0})
    }, e.n = function (t) {
        var n = t && t.__esModule ? function () {
            return t.default
        } : function () {
            return t
        };
        return e.d(n, "a", n), n
    }, e.o = function (t, n) {
        return Object.prototype.hasOwnProperty.call(t, n)
    }, e.p = "", e(e.s = 210)
}({
    0: function (t, n) {
        t.exports = {
            BEHAVIOR_PREFIX: "behavior_",
            JS_HOOK: "data-js-hook",
            noopFunct: function () {
            },
            STATE_PREFIX: "state_",
            UNDEFINED: void 0
        }
    }, 1: function (t, n, e) {
        var i = e(3), r = e(0).STATE_PREFIX + "atomic_init";
        t.exports = {
            checkDom: function (t, n) {
                return function (t, n) {
                    if (!t || !t.classList) throw new Error(t + ' is not valid. Check that element is a DOM node with class "' + n + '"')
                }(t, n), function (t, n) {
                    var e = t.classList.contains(n) ? t : t.querySelector("." + n);
                    if (!e) throw new Error(n + " not found on or in passed DOM node.");
                    return e
                }(t, n)
            }, destroyInitFlag: function (t) {
                return !!i.contains(t, r) && (i.remove(t, r), !0)
            }, instantiateAll: function (t, n) {
                for (var e, i = document.querySelectorAll(t), r = [], o = 0, s = i.length; o < s; o++) (e = new n(i[o])).init(), r.push(e);
                return r
            }, setInitFlag: function (t) {
                return !i.contains(t, r) && (i.add(t, r), !0)
            }
        }
    }, 209: function (t, n, e) {
        var i = e(1), r = e(24);
        i.instantiateAll(".m-notification", r)
    }, 210: function (t, n, e) {
        t.exports = e(209)
    }, 24: function (t, n, e) {
        var i = e(1), r = e(0);
        t.exports = function (t) {
            var n, e = "m-notification", o = "success", s = "warning", u = "error",
                c = e + "__visible", a = i.checkDom(t, e),
                f = a.querySelector("." + e + "_content");

            function l(t, n) {
                var e = '<p class="h4 m-notification_message">' + t + "</p>";
                return void 0 !== n && (e += '<p class="h4 m-notification_explanation">' + n + "</p>"), f.innerHTML = e, this
            }

            return this.SUCCESS = o, this.WARNING = s, this.ERROR = u, this.init = function () {
                if (!i.setInitFlag(a)) return r.UNDEFINED;
                var t = a.classList;
                return t.contains(e + "__" + o) ? n = o : t.contains(e + "__" + s) ? n = s : t.contains(e + "__" + u) && (n = u), this
            }, this.setContent = l, this.setTypeAndContent = function (t, i, r) {
                return function (t) {
                    if (n === t) return this;
                    var i = a.classList;
                    if (i.remove(e + "__" + n), t !== o && t !== s && t !== u) throw new Error(t + " is not a supported notification type!");
                    i.add(e + "__" + t), n = t
                }(t), l(i, r), this
            }, this.show = function () {
                return n === u || n === s ? f.setAttribute("role", "alert") : f.removeAttribute("role"), a.classList.add(c), this
            }, this.hide = function () {
                return a.classList.remove(c), this
            }, this
        }
    }, 3: function (t, n, e) {
        var i = e(0);
        t.exports = {
            add: function (t, n) {
                if (-1 !== n.indexOf(" ")) {
                    var e = i.JS_HOOK + " values cannot contain spaces!";
                    throw new Error(e)
                }
                var r = t.getAttribute(i.JS_HOOK);
                return null !== r && (n = r + " " + n), t.setAttribute(i.JS_HOOK, n), n
            }, contains: function (t, n) {
                if (!t) return !1;
                var e = t.getAttribute(i.JS_HOOK);
                return !!e && (e = e.split(" ")).indexOf(n) > -1
            }, remove: function (t, n) {
                var e = t.getAttribute(i.JS_HOOK), r = e.indexOf(n), o = e.split(" ");
                return r > -1 && (o.splice(r, 1), t.setAttribute(i.JS_HOOK, o.join(" ")), !0)
            }
        }
    }
});