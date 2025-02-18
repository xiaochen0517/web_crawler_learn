var at

const Ri = function (t) {
    return null != t && (Li(t) || function (t) {
        return "function" == typeof t.readFloatLE && "function" == typeof t.slice && Li(t.slice(0, 0))
    }(t) || !!t._isBuffer)
};

const Ti = {
    utf8: {
        stringToBytes: function (t) {
            return Pi.bin.stringToBytes(unescape(encodeURIComponent(t)))
        },
        bytesToString: function (t) {
            return decodeURIComponent(escape(Pi.bin.bytesToString(t)))
        }
    },
    bin: {
        stringToBytes: function (t) {
            for (var e = [], n = 0; n < t.length; n++)
                e.push(255 & t.charCodeAt(n));
            return e
        },
        bytesToString: function (t) {
            for (var e = [], n = 0; n < t.length; n++)
                e.push(String.fromCharCode(t[n]));
            return e.join("")
        }
    }
};
const Pi = Ti;

const Ei = {
    rotl: function (t, e) {
        return t << e | t >>> 32 - e
    },
    rotr: function (t, e) {
        return t << 32 - e | t >>> e
    },
    endian: function (t) {
        if (t.constructor == Number)
            return 16711935 & Ei.rotl(t, 8) | 4278255360 & Ei.rotl(t, 24);
        for (var e = 0; e < t.length; e++)
            t[e] = Ei.endian(t[e]);
        return t
    },
    randomBytes: function (t) {
        for (var e = []; t > 0; t--)
            e.push(Math.floor(256 * Math.random()));
        return e
    },
    bytesToWords: function (t) {
        for (var e = [], n = 0, r = 0; n < t.length; n++,
            r += 8)
            e[r >>> 5] |= t[n] << 24 - r % 32;
        return e
    },
    wordsToBytes: function (t) {
        for (var e = [], n = 0; n < 32 * t.length; n += 8)
            e.push(t[n >>> 5] >>> 24 - n % 32 & 255);
        return e
    },
    bytesToHex: function (t) {
        for (var e = [], n = 0; n < t.length; n++)
            e.push((t[n] >>> 4).toString(16)),
                e.push((15 & t[n]).toString(16));
        return e.join("")
    },
    hexToBytes: function (t) {
        for (var e = [], n = 0; n < t.length; n += 2)
            e.push(parseInt(t.substr(n, 2), 16));
        return e
    },
    bytesToBase64: function (t) {
        for (var e = [], n = 0; n < t.length; n += 3)
            for (var r = t[n] << 16 | t[n + 1] << 8 | t[n + 2], i = 0; i < 4; i++)
                8 * n + 6 * i <= 8 * t.length ? e.push(_i.charAt(r >>> 6 * (3 - i) & 63)) : e.push("=");
        return e.join("")
    },
    base64ToBytes: function (t) {
        t = t.replace(/[^A-Z0-9+\/]/gi, "");
        for (var e = [], n = 0, r = 0; n < t.length; r = ++n % 4)
            0 != r && e.push((_i.indexOf(t.charAt(n - 1)) & Math.pow(2, -2 * r + 8) - 1) << 2 * r | _i.indexOf(t.charAt(n)) >>> 6 - 2 * r);
        return e
    }
};

const ji = Ei;

!function () {
    var t = ji
        , e = Ti.utf8
        , n = Ri
        , r = Ti.bin
        , i = function i(o, a) {
        o.constructor == String ? o = a && "binary" === a.encoding ? r.stringToBytes(o) : e.stringToBytes(o) : n(o) ? o = Array.prototype.slice.call(o, 0) : Array.isArray(o) || o.constructor === Uint8Array || (o = o.toString());
        for (var s = t.bytesToWords(o), c = 8 * o.length, u = 1732584193, l = -271733879, f = -1732584194, d = 271733878, p = 0; p < s.length; p++)
            s[p] = 16711935 & (s[p] << 8 | s[p] >>> 24) | 4278255360 & (s[p] << 24 | s[p] >>> 8);
        s[c >>> 5] |= 128 << c % 32,
            s[14 + (c + 64 >>> 9 << 4)] = c;
        var h = i._ff
            , v = i._gg
            , m = i._hh
            , y = i._ii;
        for (p = 0; p < s.length; p += 16) {
            var g = u
                , b = l
                , w = f
                , A = d;
            u = h(u, l, f, d, s[p + 0], 7, -680876936),
                d = h(d, u, l, f, s[p + 1], 12, -389564586),
                f = h(f, d, u, l, s[p + 2], 17, 606105819),
                l = h(l, f, d, u, s[p + 3], 22, -1044525330),
                u = h(u, l, f, d, s[p + 4], 7, -176418897),
                d = h(d, u, l, f, s[p + 5], 12, 1200080426),
                f = h(f, d, u, l, s[p + 6], 17, -1473231341),
                l = h(l, f, d, u, s[p + 7], 22, -45705983),
                u = h(u, l, f, d, s[p + 8], 7, 1770035416),
                d = h(d, u, l, f, s[p + 9], 12, -1958414417),
                f = h(f, d, u, l, s[p + 10], 17, -42063),
                l = h(l, f, d, u, s[p + 11], 22, -1990404162),
                u = h(u, l, f, d, s[p + 12], 7, 1804603682),
                d = h(d, u, l, f, s[p + 13], 12, -40341101),
                f = h(f, d, u, l, s[p + 14], 17, -1502002290),
                u = v(u, l = h(l, f, d, u, s[p + 15], 22, 1236535329), f, d, s[p + 1], 5, -165796510),
                d = v(d, u, l, f, s[p + 6], 9, -1069501632),
                f = v(f, d, u, l, s[p + 11], 14, 643717713),
                l = v(l, f, d, u, s[p + 0], 20, -373897302),
                u = v(u, l, f, d, s[p + 5], 5, -701558691),
                d = v(d, u, l, f, s[p + 10], 9, 38016083),
                f = v(f, d, u, l, s[p + 15], 14, -660478335),
                l = v(l, f, d, u, s[p + 4], 20, -405537848),
                u = v(u, l, f, d, s[p + 9], 5, 568446438),
                d = v(d, u, l, f, s[p + 14], 9, -1019803690),
                f = v(f, d, u, l, s[p + 3], 14, -187363961),
                l = v(l, f, d, u, s[p + 8], 20, 1163531501),
                u = v(u, l, f, d, s[p + 13], 5, -1444681467),
                d = v(d, u, l, f, s[p + 2], 9, -51403784),
                f = v(f, d, u, l, s[p + 7], 14, 1735328473),
                u = m(u, l = v(l, f, d, u, s[p + 12], 20, -1926607734), f, d, s[p + 5], 4, -378558),
                d = m(d, u, l, f, s[p + 8], 11, -2022574463),
                f = m(f, d, u, l, s[p + 11], 16, 1839030562),
                l = m(l, f, d, u, s[p + 14], 23, -35309556),
                u = m(u, l, f, d, s[p + 1], 4, -1530992060),
                d = m(d, u, l, f, s[p + 4], 11, 1272893353),
                f = m(f, d, u, l, s[p + 7], 16, -155497632),
                l = m(l, f, d, u, s[p + 10], 23, -1094730640),
                u = m(u, l, f, d, s[p + 13], 4, 681279174),
                d = m(d, u, l, f, s[p + 0], 11, -358537222),
                f = m(f, d, u, l, s[p + 3], 16, -722521979),
                l = m(l, f, d, u, s[p + 6], 23, 76029189),
                u = m(u, l, f, d, s[p + 9], 4, -640364487),
                d = m(d, u, l, f, s[p + 12], 11, -421815835),
                f = m(f, d, u, l, s[p + 15], 16, 530742520),
                u = y(u, l = m(l, f, d, u, s[p + 2], 23, -995338651), f, d, s[p + 0], 6, -198630844),
                d = y(d, u, l, f, s[p + 7], 10, 1126891415),
                f = y(f, d, u, l, s[p + 14], 15, -1416354905),
                l = y(l, f, d, u, s[p + 5], 21, -57434055),
                u = y(u, l, f, d, s[p + 12], 6, 1700485571),
                d = y(d, u, l, f, s[p + 3], 10, -1894986606),
                f = y(f, d, u, l, s[p + 10], 15, -1051523),
                l = y(l, f, d, u, s[p + 1], 21, -2054922799),
                u = y(u, l, f, d, s[p + 8], 6, 1873313359),
                d = y(d, u, l, f, s[p + 15], 10, -30611744),
                f = y(f, d, u, l, s[p + 6], 15, -1560198380),
                l = y(l, f, d, u, s[p + 13], 21, 1309151649),
                u = y(u, l, f, d, s[p + 4], 6, -145523070),
                d = y(d, u, l, f, s[p + 11], 10, -1120210379),
                f = y(f, d, u, l, s[p + 2], 15, 718787259),
                l = y(l, f, d, u, s[p + 9], 21, -343485551),
                u = u + g >>> 0,
                l = l + b >>> 0,
                f = f + w >>> 0,
                d = d + A >>> 0
        }
        return t.endian([u, l, f, d])
    };
    i._ff = function (t, e, n, r, i, o, a) {
        var s = t + (e & n | ~e & r) + (i >>> 0) + a;
        return (s << o | s >>> 32 - o) + e
    }
        ,
        i._gg = function (t, e, n, r, i, o, a) {
            var s = t + (e & r | n & ~r) + (i >>> 0) + a;
            return (s << o | s >>> 32 - o) + e
        }
        ,
        i._hh = function (t, e, n, r, i, o, a) {
            var s = t + (e ^ n ^ r) + (i >>> 0) + a;
            return (s << o | s >>> 32 - o) + e
        }
        ,
        i._ii = function (t, e, n, r, i, o, a) {
            var s = t + (n ^ (e | ~r)) + (i >>> 0) + a;
            return (s << o | s >>> 32 - o) + e
        }
        ,
        i._blocksize = 16,
        i._digestsize = 16,
        at = function (e, n) {
            if (null == e)
                throw new Error("Illegal argument " + e);
            var o = t.wordsToBytes(i(e, n));
            return n && n.asBytes ? o : n && n.asString ? r.bytesToString(o) : t.bytesToHex(o)
        }
}();

function ft(e) {
    return e.substring(e.lastIndexOf("/") + 1, e.length).split(".")[0]
}

var ct = "wbi_img_urls";

var keys_param = {
    wbiImgKey: "839c8b697b0d44dc80e9a604592bb432",
    wbiSubKey: "02cd020b04d64aacad6b3a08d06f8eb0"
}

var local_storage = "";

function lt(e) {
    var t, r, n = function (e) {
        var t;
        if (e.useAssignKey)
            return {
                imgKey: e.wbiImgKey,
                subKey: e.wbiSubKey
            };
        var r = (null === (t = function (e) {
            try {
                return local_storage
            } catch (e) {
                return null
            }
        }(ct)) || void 0 === t ? void 0 : t.split("-")) || []
            , n = r[0]
            , o = r[1]
            , i = n ? ft(n) : e.wbiImgKey
            , a = o ? ft(o) : e.wbiSubKey;
        return {
            imgKey: i,
            subKey: a
        }
    }(keys_param), o = n.imgKey, i = n.subKey;
    if (o && i) {
        for (var a = (t = o + i,
            r = [],
            [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52].forEach((function (e) {
                    t.charAt(e) && r.push(t.charAt(e))
                }
            )),
            r.join("").slice(0, 32)), u = 1739876385, s = Object.assign({}, e, {
            // r.join("").slice(0, 32)), u = Math.round(Date.now() / 1e3), s = Object.assign({}, e, {
            wts: u
        }), c = Object.keys(s).sort(), l = [], f = /[!'()*]/g, d = 0; d < c.length; d++) {
            var p = c[d]
                , h = s[p];
            h && "string" == typeof h && (h = h.replace(f, "")),
            null != h && l.push("".concat(encodeURIComponent(p), "=").concat(encodeURIComponent(h)))
        }
        var y = l.join("&");
        return {
            w_rid: at(y + a),
            wts: u.toString()
        }
    }
    return null
}

function get_w_rid(lt_data, local_data) {
    local_storage = local_data;
    return lt(lt_data);
}

console.log(get_w_rid(
        {
            mode: 3,
            oid: "114008111717942",
            pagination_str: `{"offset":"{\\"type\\":1,\\"direction\\":1,\\"session_id\\":\\"1781632233771436\\",\\"data\\":{}}"}`,
            plat: 1,
            // seek_rpid: "",
            type: 1,
            web_location: 1315875
        },
        "https://i0.hdslb.com/bfs/wbi/7cd084941338484aae1ad9425b84077c.png-https://i0.hdslb.com/bfs/wbi/4932caff0ff746eab6f01bf08b70ac45.png"
    )
);

// mode=3&oid=114008111717942&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts=1739786436