!function (t) {
    var e = {};

    function n(i) {
        if (e[i]) return e[i].exports;
        var r = e[i] = {i: i, l: !1, exports: {}};
        return t[i].call(r.exports, r, r.exports, n), r.l = !0, r.exports
    }

    n.m = t, n.c = e, n.d = function (t, e, i) {
        n.o(t, e) || Object.defineProperty(t, e, {
            configurable: !1,
            enumerable: !0,
            get: i
        })
    }, n.r = function (t) {
        Object.defineProperty(t, "__esModule", {value: !0})
    }, n.n = function (t) {
        var e = t && t.__esModule ? function () {
            return t.default
        } : function () {
            return t
        };
        return n.d(e, "a", e), e
    }, n.o = function (t, e) {
        return Object.prototype.hasOwnProperty.call(t, e)
    }, n.p = "", n(n.s = 208)
}({
    0: function (t, e) {
        t.exports = {
            BEHAVIOR_PREFIX: "behavior_",
            JS_HOOK: "data-js-hook",
            noopFunct: function () {
            },
            STATE_PREFIX: "state_",
            UNDEFINED: void 0
        }
    }, 1: function (t, e, n) {
        var i = n(3), r = n(0).STATE_PREFIX + "atomic_init";
        t.exports = {
            checkDom: function (t, e) {
                return function (t, e) {
                    if (!t || !t.classList) throw new Error(t + ' is not valid. Check that element is a DOM node with class "' + e + '"')
                }(t, e), function (t, e) {
                    var n = t.classList.contains(e) ? t : t.querySelector("." + e);
                    if (!n) throw new Error(e + " not found on or in passed DOM node.");
                    return n
                }(t, e)
            }, destroyInitFlag: function (t) {
                return !!i.contains(t, r) && (i.remove(t, r), !0)
            }, instantiateAll: function (t, e) {
                for (var n, i = document.querySelectorAll(t), r = [], o = 0, s = i.length; o < s; o++) (n = new e(i[o])).init(), r.push(n);
                return r
            }, setInitFlag: function (t) {
                return !i.contains(t, r) && (i.add(t, r), !0)
            }
        }
    }, 11: function (t, e) {
        t.exports = {
            bpXS: {min: 0, max: 600},
            bpSM: {min: 601, max: 900},
            bpMED: {min: 901, max: 1020},
            bpLG: {min: 1021, max: 1200},
            bpXL: {min: 1201}
        }
    }, 13: function (t, e) {
        t.exports = {
            getViewportDimensions: function () {
                var t = window, e = "inner";
                return "innerWidth" in window || (t = document.documentElement || document.body, e = "client"), {
                    width: t[e + "Width"],
                    height: t[e + "Height"]
                }
            }
        }
    }, 148: function (t, e, n) {
        var i = n(22), r = n(7).get,
            o = document.querySelectorAll(".o-expandable__read-more");
        if (o && r().isBpXS) for (var s = function (t) {
            var e = o[t], n = new i(e).init();
            n.addEventListener("expandEnd", function () {
                n.destroy(), e.querySelector(".o-expandable_content").style.height = ""
            })
        }, a = 0; a < o.length; a++) s(a)
    }, 2: function (t, e) {
        t.exports = function t() {
            var e = {};
            return t.prototype.addEventListener = function (t, n) {
                return e.hasOwnProperty(t) ? e[t].push(n) : e[t] = [n], this
            }, t.prototype.removeEventListener = function (t, n) {
                if (!e.hasOwnProperty(t)) return this;
                var i = e[t].indexOf(n);
                return -1 !== i && e[t].splice(i, 1), this
            }, t.prototype.dispatchEvent = function (t, n) {
                if (!e.hasOwnProperty(t)) return this;
                n = n || {};
                for (var i = e[t], r = 0, o = i.length; r < o; r++) i[r].call(this, n);
                return this
            }, this
        }
    }, 208: function (t, e, n) {
        t.exports = n(148)
    }, 22: function (t, e, n) {
        var i = n(1), r = n(7), o = n(2), s = n(0);

        function a(t, e, n) {
            return n > e ? e : n < t ? t : n
        }

        t.exports = function (t) {
            var e, n, u = "o-expandable", c = 0, d = 1, f = 2, v = 3,
                h = i.checkDom(t, u), p = h.querySelector("." + u + "_target"),
                l = h.querySelector("." + u + "_content"),
                E = l.querySelector("." + u + "_content-animated"),
                m = h.querySelector("." + u + "_link"), b = c, O = function (t) {
                    var e, n = {
                        WebkitTransition: "webkitTransitionEnd",
                        MozTransition: "transitionend",
                        OTransition: "oTransitionEnd otransitionend",
                        transition: "transitionend"
                    };
                    for (var i in n) if (n.hasOwnProperty(i) && void 0 !== t.style[i]) {
                        e = n[i];
                        break
                    }
                    return e
                }(l), g = (e = {
                    webkitTransitionEnd: "-webkit-transition",
                    MozTransition: "-moz-transition",
                    OTransition: "-o-transition",
                    transitionend: "transition"
                })[O] || e.transitionend, w = this, x = D.bind(this), L = A.bind(this),
                y = {disconnect: s.noopFunct};

            function _() {
                (y = new MutationObserver(function (t) {
                    t.forEach(I)
                })).observe(l, {childList: !0, subtree: !0})
            }

            function S() {
                l.addEventListener("DOMNodeInserted", I), l.addEventListener("DOMNodeRemoved", I)
            }

            function A(t) {
                return J() || b === f ? this : (t = t || a(225, 450, n) / 1e3, z(f), this.dispatchEvent("expandBegin", {target: w}), q(), M(P, t), this)
            }

            function D(t) {
                return K() || b === d ? this : (t = t || a(175, 450, n / 2) / 1e3, z(d), this.dispatchEvent("collapseBegin", {target: w}), B(), M(F, t), this)
            }

            function I() {
                J() ? q() : B()
            }

            function M(t, e) {
                O ? (l.addEventListener(O, t), l.style[g] = "height " + e + "s ease-out") : t()
            }

            function T() {
                h.classList.add(u + "__expanded"), l.setAttribute("aria-expanded", "true"), p.setAttribute("aria-pressed", "true"), z(v)
            }

            function k() {
                h.classList.remove(u + "__expanded"), l.setAttribute("aria-expanded", "false"), p.setAttribute("aria-pressed", "false"), z(c)
            }

            function P() {
                l.removeEventListener(O, P), T(), w.dispatchEvent("expandEnd", {target: w})
            }

            function F() {
                l.removeEventListener(O, F), k(), w.dispatchEvent("collapseEnd", {target: w})
            }

            function H() {
                w.dispatchEvent("click", {target: w}), (K() || J()) && w.toggle()
            }

            function N() {
                n = E.offsetHeight
            }

            function X() {
                E.offsetHeight !== n && (I(), R() && x())
            }

            function q() {
                N(), l.style.height = n + "px"
            }

            function B() {
                l.style.height = "0"
            }

            function K() {
                return b === c
            }

            function J() {
                return b === v
            }

            function z(t) {
                return b = t
            }

            function R() {
                var t = !1;
                return r.get().isBpXS && (t = !0), t
            }

            var j = new o;
            return this.addEventListener = j.addEventListener, this.removeEventListener = j.removeEventListener, this.dispatchEvent = j.dispatchEvent, this.init = function (t) {
                return i.setInitFlag(h) ? (N(), R() || t !== v && "expanded" !== h.getAttribute("data-state") ? k() : (q(), T()), m.classList.remove("u-hidden"), p.addEventListener("click", H), h.getAttribute("data-read-more") || window.addEventListener("resize", X), e = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver ? _ : S, window.setTimeout(e, 0), this) : s.UNDEFINED;
                var e
            }, this.toggle = function (t) {
                return J() ? x(t) : L(t), w
            }, this.expand = A, this.refreshHeight = I, this.collapse = D, this.destroy = function () {
                return i.destroyInitFlag(h) && (p.removeEventListener("click", H), window.removeEventListener("resize", X), l.removeEventListener("DOMNodeInserted", I, !1), l.removeEventListener("DOMNodeRemoved", I, !1), y.disconnect()), this
            }, this.COLLAPSED = c, this.EXPANDED = v, this
        }
    }, 3: function (t, e, n) {
        var i = n(0);
        t.exports = {
            add: function (t, e) {
                if (-1 !== e.indexOf(" ")) {
                    var n = i.JS_HOOK + " values cannot contain spaces!";
                    throw new Error(n)
                }
                var r = t.getAttribute(i.JS_HOOK);
                return null !== r && (e = r + " " + e), t.setAttribute(i.JS_HOOK, e), e
            }, contains: function (t, e) {
                if (!t) return !1;
                var n = t.getAttribute(i.JS_HOOK);
                return !!n && (n = n.split(" ")).indexOf(e) > -1
            }, remove: function (t, e) {
                var n = t.getAttribute(i.JS_HOOK), r = n.indexOf(e), o = n.split(" ");
                return r > -1 && (o.splice(r, 1), t.setAttribute(i.JS_HOOK, o.join(" ")), !0)
            }
        }
    }, 7: function (t, e, n) {
        var i = n(11), r = n(13).getViewportDimensions;

        function o(t, e) {
            var n = t.min || 0, i = t.max || Number.POSITIVE_INFINITY;
            return n <= e && e <= i
        }

        function s(t) {
            var e = {};
            for (var n in t = t || r().width, i) e["is" + n.charAt(0).toUpperCase() + n.slice(1)] = o(i[n], t);
            return e
        }

        t.exports = {
            get: s, isInDesktop: function () {
                var t = !1, e = s();
                return (e.isBpMED || e.isBpLG || e.isBpXL) && (t = !0), t
            }
        }
    }
});