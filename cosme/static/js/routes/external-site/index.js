!function (t) {
    var n = {};

    function e(r) {
        if (n[r]) return n[r].exports;
        var o = n[r] = {i: r, l: !1, exports: {}};
        return t[r].call(o.exports, o, o.exports, e), o.l = !0, o.exports
    }

    e.m = t, e.c = n, e.d = function (t, n, r) {
        e.o(t, n) || Object.defineProperty(t, n, {
            configurable: !1,
            enumerable: !0,
            get: r
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
    }, e.p = "", e(e.s = 251)
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
        var r = e(3), o = e(0).STATE_PREFIX + "atomic_init";
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
                return !!r.contains(t, o) && (r.remove(t, o), !0)
            }, instantiateAll: function (t, n) {
                for (var e, r = document.querySelectorAll(t), o = [], i = 0, c = r.length; i < c; i++) (e = new n(r[i])).init(), o.push(e);
                return o
            }, setInitFlag: function (t) {
                return !r.contains(t, o) && (r.add(t, o), !0)
            }
        }
    }, 249: function (t, n, e) {
        var r = e(1);
        t.exports = function (t) {
            var n, e = r.checkDom(t, "external-site_container"),
                o = e.querySelector(".external-site_reload-container"),
                i = e.querySelector(".external-site_proceed-btn"), c = 5;

            function u() {
                var t;
                t = "<span class='external-site_reload-duration'>" + c + "</span> second" + (1 === c ? "" : "s"), o.innerHTML = t, 0 == --c && a()
            }

            function a() {
                var t = e.querySelector("form#proceed");
                clearInterval(n), t.submit()
            }

            function s(t) {
                t.stopImmediatePropagation(), a()
            }

            return this.init = function () {
                n = setInterval(u, 1e3), i.addEventListener("click", s)
            }, this
        }
    }, 250: function (t, n, e) {
        new (e(249))(document.querySelector(".external-site_container")).init()
    }, 251: function (t, n, e) {
        t.exports = e(250)
    }, 3: function (t, n, e) {
        var r = e(0);
        t.exports = {
            add: function (t, n) {
                if (-1 !== n.indexOf(" ")) {
                    var e = r.JS_HOOK + " values cannot contain spaces!";
                    throw new Error(e)
                }
                var o = t.getAttribute(r.JS_HOOK);
                return null !== o && (n = o + " " + n), t.setAttribute(r.JS_HOOK, n), n
            }, contains: function (t, n) {
                if (!t) return !1;
                var e = t.getAttribute(r.JS_HOOK);
                return !!e && (e = e.split(" ")).indexOf(n) > -1
            }, remove: function (t, n) {
                var e = t.getAttribute(r.JS_HOOK), o = e.indexOf(n), i = e.split(" ");
                return o > -1 && (i.splice(o, 1), t.setAttribute(r.JS_HOOK, i.join(" ")), !0)
            }
        }
    }
});