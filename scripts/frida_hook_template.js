// 通用 Frida Hook 模板
// 用法: frida -U -f com.example.app -l frida_hook_template.js --no-pause
// 仅用于自己拥有或获得授权的应用分析。

Java.perform(function () {
    var TAG = '[hook]';

    // 1) Hook 指定类的全部重载
    function hookAll(clsName, methodName) {
        try {
            var Cls = Java.use(clsName);
            var overloads = Cls[methodName].overloads;
            overloads.forEach(function (overload) {
                overload.implementation = function () {
                    var args = [];
                    for (var i = 0; i < arguments.length; i++) {
                        args.push(String(arguments[i]));
                    }
                    console.log(TAG + ' ' + clsName + '.' + methodName + '(' + args.join(', ') + ')');
                    var ret = overload.apply(this, arguments);
                    console.log(TAG + '  -> ' + ret);
                    return ret;
                };
            });
            console.log(TAG + ' hooked ' + clsName + '.' + methodName);
        } catch (e) {
            console.log(TAG + ' hook failed ' + clsName + '.' + methodName + ': ' + e);
        }
    }

    // 2) Hook 返回字符串的方法，便于观察签名/加密结果
    function traceStringReturn(clsName, methodName) {
        try {
            var Cls = Java.use(clsName);
            Cls[methodName].overloads.forEach(function (overload) {
                overload.implementation = function () {
                    var ret = overload.apply(this, arguments);
                    if (typeof ret === 'string') {
                        console.log(TAG + ' ' + clsName + '.' + methodName + ' => ' + ret);
                    }
                    return ret;
                };
            });
        } catch (e) {
            console.log(TAG + ' trace failed: ' + e);
        }
    }

    // 示例（按目标替换）
    // hookAll('com.example.net.SignHelper', 'sign');
    // traceStringReturn('com.example.net.Api', 'encrypt');

    // 3) Native 导出函数 Hook（可跨 so）
    function hookNative(moduleName, symbol) {
        var addr = Module.findExportByName(moduleName, symbol);
        if (!addr) { console.log(TAG + ' symbol not found: ' + moduleName + '!' + symbol); return; }
        Interceptor.attach(addr, {
            onEnter: function (args) {
                console.log(TAG + ' ' + symbol + ' called; arg0=' + args[0]);
            },
            onLeave: function (retval) {
                console.log(TAG + ' ' + symbol + ' ret=' + retval);
            }
        });
    }
    // hookNative('libnative.so', 'Java_com_example_Native_sign');

    // 4) 枚举已加载类中含关键词的类，快速定位
    function findClasses(keyword) {
        Java.enumerateLoadedClasses({
            onMatch: function (name) {
                if (name.toLowerCase().indexOf(keyword.toLowerCase()) >= 0) console.log(TAG + ' class: ' + name);
            },
            onComplete: function () { console.log(TAG + ' enumerate done'); }
        });
    }
    // findClasses('sign');
});
