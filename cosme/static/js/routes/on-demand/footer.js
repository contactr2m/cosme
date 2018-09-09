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
    }, e.p = "", e(e.s = 226)
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
                for (var e, r = document.querySelectorAll(t), o = [], i = 0, u = r.length; i < u; i++) (e = new n(r[i])).init(), o.push(e);
                return o
            }, setInitFlag: function (t) {
                return !r.contains(t, o) && (r.add(t, o), !0)
            }
        }
    }, 149: function (t, n, e) {
        "use strict";
        var r = function (t) {
            if (t && t.__esModule) return t;
            var n = {};
            if (null != t) for (var e in t) Object.prototype.hasOwnProperty.call(t, e) && (n[e] = t[e]);
            return n.default = t, n
        }(e(60));
        t.exports = {
            init: function () {
                r.attach("return-to-top", "click", function (t) {
                    var n, e, r, o, i;
                    t.preventDefault(), e = window.scrollY, r = Math.PI / 30, o = e / 2, i = 0, "requestAnimationFrame" in window != 0 ? window.requestAnimationFrame(function t() {
                        0 !== window.scrollY && window.setTimeout(function () {
                            i += 1;
                            var u = o * Math.cos(i * r);
                            n = o - u, window.scrollTo(0, e - n), window.requestAnimationFrame(t)
                        }, 10)
                    }) : window.scrollTo(0, 0)
                })
            }
        }
    }, 150: function (t, n, e) {
        var r = e(1), o = e(149), i = e(0);
        t.exports = function (t) {
            var n = r.checkDom(t, "o-footer");
            return this.init = function () {
                return r.setInitFlag(n) ? (o.init(), this) : i.UNDEFINED
            }, this
        }
    }, 225: function (t, n, e) {
        new (e(150))(document.body).init()
    }, 226: function (t, n, e) {
        t.exports = e(225)
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
    }, 60: function (t, n, e) {
        var r = e(0), o = e(3);

        function i(t, n) {
            n = n || document;
            var e = [];
            try {
                e = n.querySelectorAll(t)
            } catch (n) {
                throw new Error(t + " not found in DOM!")
            }
            return 0 === e.length && -1 === t.indexOf(r.BEHAVIOR_PREFIX) && (e = u(t, n)), e
        }

        function u(t, n) {
            return i(t = "[" + (t = r.JS_HOOK + "*=" + r.BEHAVIOR_PREFIX + t) + "]", n)
        }

        t.exports = {
            attach: function (t, n, e, r) {
                var o = [];
                t instanceof NodeList == 1 ? o = t : t instanceof Node == 1 ? o = [t] : "string" == typeof t && (o = i(t, r));
                for (var u = 0, c = o.length; u < c; u++) o[u].addEventListener(n, e, !1);
                return o
            }, checkBehaviorDom: function (t, n) {
                var e;
                if (o.contains(t, n)) return t;
                if (t) {
                    var i = "[" + r.JS_HOOK + "=" + n + "]";
                    e = t.querySelector(i)
                }
                if (!e) throw new Error(n + " behavior not found on passed DOM node!");
                return e
            }, find: u, remove: function (t, n, e) {
                t.removeEventListener(n, e)
            }
        }
    }
});