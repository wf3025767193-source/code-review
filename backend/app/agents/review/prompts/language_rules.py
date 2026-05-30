"""Language-specific review rules for specialist agents."""

LANGUAGE_RULES = {
    "py": {
        "security": "Python: 警惕 eval/exec/os.system 注入、pickle 反序列化攻击、JWT alg=none 绕过、SSTI 模板注入。Django/Flask: 检查 DEBUG 模式泄露、CSRF 保护缺失、ORM 注入。",
        "performance": "Python: 注意 GIL 下 CPU 密集操作阻塞事件循环、同步 HTTP/DB 调用未放线程池、大列表推导内存膨胀、循环内字符串拼接。",
        "style": "Python: 检查 PEP 8 命名规范、缺失 type hints、f-string 优先于 % 格式化、上下文管理器 with 使用、裸 except 捕获。",
    },
    "js": {
        "security": "JavaScript: 警惕 XSS (innerHTML)、原型污染、eval/Function 注入、不安全的 JSONP、CORS 配置过宽、npm 包投毒。Node: 检查 child_process exec 注入、路径遍历。",
        "performance": "JavaScript: 注意 Promise.all 并行机会、防抖节流缺失、大列表虚拟滚动、闭包内存泄漏、console.log 生产残留。",
        "style": "JavaScript: 检查 const/let 使用、=== 严格相等、async/await 优于 then、可选链 ?. 使用、魔法数字提取常量。",
    },
    "ts": {
        "security": "TypeScript: 同 JS + 警惕 any 类型绕过类型安全检查、类型断言未验证、装饰器注入。Node: 同 JS Node 规则。",
        "performance": "TypeScript: 注意类型体操过于复杂影响编译速度、大接口类型递归。其余同 JavaScript 性能规则。",
        "style": "TypeScript: 检查 any 滥用、接口 vs type 一致性、泛型命名规范、严格模式启用、enum vs const assertion 选择。",
    },
    "java": {
        "security": "Java: 警惕 SQL 注入 (JDBC PreparedStatement 缺失)、XXE (XML 解析器未禁用)、反序列化漏洞、Log4j 注入。Spring: 检查 CSRF 保护、SpEL 注入、actuator 端点暴露。",
        "performance": "Java: 注意 N+1 查询 (Hibernate)、连接池未释放、StringBuilder vs String 拼接、不必要的同步锁争用、Stream API 短路操作缺失。",
        "style": "Java: 检查命名规范 (camelCase)、Lombok 合理使用、Optional 优于 null、try-with-resources、不可变对象优先。",
    },
    "go": {
        "security": "Go: 警惕 SQL 注入、命令注入 (os/exec)、模板注入 (html/template vs text/template)、整数溢出、HTTP 请求 SSRF。检查 crypto/rand 用于密钥生成而非 math/rand。",
        "performance": "Go: 注意 goroutine 泄漏、channel 死锁、sync.Pool 复用、不必要的内存分配 (逃逸分析)、连接池大小配置。",
        "style": "Go: 检查 error 处理 (不忽略)、命名规范 (驼峰)、包组织、defer 使用、interface 小接口原则、context 传递。",
    },
    "sql": {
        "security": "SQL: 警惕拼接查询 (防 SQL 注入)、敏感数据明文存储、缺少行级权限、未加密备份。检查 GRANT 权限最小化。",
        "performance": "SQL: 注意缺少索引、SELECT * 全表扫描、大表 JOIN 无限制、子查询未优化、连接池配置不当、N+1 查询模式。",
        "style": "SQL: 检查关键字大小写一致性、表/列命名规范、注释缺失、存储过程过长、事务边界不明确。",
    },
}

_UNKNOWN_RULES = {
    "security": "检查通用安全风险：输入验证、输出编码、权限控制、敏感数据保护。",
    "performance": "检查通用性能问题：不必要的资源分配、循环内重操作、缓存缺失。",
    "style": "检查通用规范：命名一致性、适当注释、合理的函数长度。",
}


def build_language_rules(languages: list[str]) -> dict[str, str]:
    """Merge language-specific rules for detected languages."""
    if not languages:
        languages = ["unknown"]

    merged = {"security": [], "performance": [], "style": []}
    seen = set()

    for lang in languages[:5]:
        rules = LANGUAGE_RULES.get(lang, _UNKNOWN_RULES)
        for key in merged:
            text = rules[key]
            if text not in seen:
                merged[key].append(text)
                seen.add(text)

    return {
        "security": " | ".join(merged["security"]) if merged["security"] else _UNKNOWN_RULES["security"],
        "performance": " | ".join(merged["performance"]) if merged["performance"] else _UNKNOWN_RULES["performance"],
        "style": " | ".join(merged["style"]) if merged["style"] else _UNKNOWN_RULES["style"],
    }
