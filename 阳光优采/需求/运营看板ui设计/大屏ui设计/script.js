/**
 * 阳光优采 - 数据可视化运营大屏 V11 (UI/UX Pro Max · Enterprise Platinum)
 */

window.addEventListener('load', () => {
    // 调色盘 - Enterprise Platinum (Deep Indigo, Emerald, Amber, Rose)
    const COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#f43f5e', '#8b5cf6', '#0ea5e9'];

    // 顶级字体排版体系
    const LABEL_STYLE = {
        color: '#64748b',
        fontWeight: 500,
        fontSize: 11,
        fontFamily: "'Plus Jakarta Sans', 'Noto Sans SC', sans-serif",
        padding: [2, 0]
    };

    // 数据特殊字体 (JetBrains Mono)
    const DATA_FONT = "'JetBrains Mono', monospace";

    // 高级毛玻璃 Tooltip
    const TOOLTIP_STYLE = {
        backgroundColor: 'rgba(255, 255, 255, 0.85)',
        borderColor: 'rgba(255, 255, 255, 1)',
        borderWidth: 1,
        padding: 12,
        borderRadius: 12,
        textStyle: { color: '#0f172a', fontFamily: "'Plus Jakarta Sans', sans-serif", fontSize: 13, fontWeight: 500 },
        extraCssText: 'box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.1), inset 0 1px 0 rgba(255,255,255,1); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);'
    };

    const formatCurrency = (val) => '¥' + val.toLocaleString('en-US', { minimumFractionDigits: 2 });

    const chartInstances = {};

    // --- 1. 月度趋势 (V11 Pro Max) ---
    const initTrend = () => {
        const el = document.getElementById('v11-trend-chart');
        if (!el) return;
        const chart = echarts.init(el);
        chart.setOption({
            backgroundColor: 'transparent',
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'line', lineStyle: { color: '#cbd5e1', width: 2, type: 'dashed' } },
                ...TOOLTIP_STYLE,
                formatter: (params) => {
                    let res = `<div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#64748b;font-weight:700;margin-bottom:8px">${params[0].name}</div>`;
                    params.forEach(p => {
                        const val = p.seriesName.includes('金额') || p.seriesName.includes('总额') ? formatCurrency(p.value) : `${p.value} 笔`;
                        res += `<div style="display:flex;align-items:center;justify-content:space-between;gap:24px;margin-bottom:4px">
                            <span style="display:flex;align-items:center;gap:6px;font-size:12px;color:#475569">
                                <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p.color}"></span>
                                ${p.seriesName}
                            </span>
                            <span style="font-family:${DATA_FONT};font-weight:800;font-size:13px;color:#0f172a">${val}</span>
                        </div>`;
                    });
                    return res;
                }
            },
            legend: {
                data: ['订单量', '成交总额 (元)'],
                top: 0,
                right: 0,
                icon: 'circle',
                itemWidth: 8,
                itemHeight: 8,
                textStyle: { ...LABEL_STYLE, color: '#475569', fontWeight: 600 }
            },
            grid: { top: 40, left: 0, right: 0, bottom: 0, containLabel: true },
            xAxis: {
                type: 'category',
                boundaryGap: true,
                data: ['08月', '09月', '12月', '01月', '02月'],
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { ...LABEL_STYLE, margin: 12 }
            },
            yAxis: [
                {
                    type: 'value',
                    splitLine: { show: false },
                    axisLabel: { show: false }
                },
                {
                    type: 'value',
                    splitLine: { lineStyle: { color: 'rgba(226,232,240,0.5)', type: 'solid' } },
                    axisLabel: {
                        ...LABEL_STYLE,
                        fontFamily: DATA_FONT,
                        formatter: (val) => val >= 1000 ? (val / 1000).toFixed(1) + 'k' : val,
                        margin: 12
                    }
                }
            ],
            series: [
                {
                    name: '订单量',
                    type: 'bar',
                    barWidth: '20%',
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#6366f1' },
                            { offset: 1, color: '#4338ca' }
                        ]),
                        borderRadius: [6, 6, 6, 6],
                        shadowColor: 'rgba(99,102,241,0.2)',
                        shadowBlur: 10,
                        shadowOffsetY: 5
                    },
                    data: [1, 1, 6, 49, 44]
                },
                {
                    name: '成交总额 (元)',
                    type: 'line',
                    yAxisIndex: 1,
                    smooth: 0.4,
                    showSymbol: false,
                    symbolSize: 8,
                    itemStyle: { color: '#059669', borderWidth: 3, borderColor: '#fff' },
                    lineStyle: { width: 4, shadowColor: 'rgba(5,150,105,0.4)', shadowBlur: 15, shadowOffsetY: 5 },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: 'rgba(5, 150, 105, 0.25)' },
                            { offset: 1, color: 'rgba(5, 150, 105, 0.01)' }
                        ])
                    },
                    data: [32, 33.8, 1435.1, 31217.5, 33027.1]
                }
            ]
        });
        chartInstances.trend = chart;
    };

    // --- 2. 专区分布 (V11 Pro Max) ---
    const initBreakdown = () => {
        const el = document.getElementById('v11-breakdown-chart');
        if (!el) return;
        const chart = echarts.init(el);
        const data = [
            { name: '中国煤地', value: 31981.45 },
            { name: '新疆阳光', value: 1045.6 },
            { name: '大连国企', value: 216.94 },
            { name: '邯郸优采', value: 33.8 }
        ];

        const total = data.reduce((sum, item) => sum + item.value, 0);

        chart.setOption({
            backgroundColor: 'transparent',
            tooltip: { 
                trigger: 'item', 
                ...TOOLTIP_STYLE,
                formatter: (p) => `<div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#64748b;font-weight:700;margin-bottom:4px">${p.name}</div><div style="font-family:${DATA_FONT};font-weight:800;font-size:14px;color:#0f172a">¥${p.value.toLocaleString()} <span style="font-size:11px;color:#64748b;font-weight:600;font-family:'Plus Jakarta Sans'">(${((p.value/total)*100).toFixed(1)}%)</span></div>`
            },
            legend: {
                orient: 'horizontal',
                bottom: '0%',
                left: 'center',
                icon: 'circle',
                itemWidth: 8,
                itemHeight: 8,
                itemGap: 12,
                formatter: (name) => {
                    const item = data.find(d => d.name === name);
                    const pct = ((item.value / total) * 100).toFixed(1);
                    return `${name} ${pct}%`;
                },
                textStyle: { 
                    fontSize: 11, color: '#475569', fontWeight: 600, fontFamily: "'Plus Jakarta Sans'"
                }
            },
            series: [{
                type: 'pie',
                radius: ['40%', '65%'], 
                center: ['50%', '42%'], 
                itemStyle: { 
                    borderRadius: 6, 
                    borderColor: '#ffffff', 
                    borderWidth: 2,
                    shadowColor: 'rgba(15,23,42,0.08)',
                    shadowBlur: 10,
                    shadowOffsetY: 4
                },
                labelLine: { show: true, length: 5, length2: 5 },
                label: { 
                    show: true, 
                    position: 'outside', 
                    formatter: '{d}%',
                    fontSize: 10,
                    fontWeight: 700,
                    color: '#64748b'
                },
                data: data,
                color: COLORS
            }]
        });
        chartInstances.breakdown = chart;
    };

    // --- 3. 供应商增长 (V11 Pro Max) ---
    const initSupplier = () => {
        const el = document.getElementById('v11-supplier-chart');
        if (!el) return;
        const chart = echarts.init(el);
        chart.setOption({
            backgroundColor: 'transparent',
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'line', lineStyle: { color: '#cbd5e1', width: 2, type: 'dashed' } },
                ...TOOLTIP_STYLE,
                formatter: (params) => {
                    const p = params[0];
                    return `<div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#64748b;font-weight:700;margin-bottom:4px">${p.name}</div><div style="display:flex;align-items:center;gap:6px"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p.color}"></span><span style="font-family:${DATA_FONT};font-weight:800;font-size:14px;color:#0f172a">${p.value} 家</span></div>`;
                }
            },
            grid: { top: 30, left: 0, right: 10, bottom: 0, containLabel: true },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: ['08月', '09月', '12月', '01月', '02月'],
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { ...LABEL_STYLE, margin: 16 }
            },
            yAxis: {
                type: 'value',
                axisLabel: { ...LABEL_STYLE, fontFamily: DATA_FONT, margin: 16 },
                splitLine: { lineStyle: { color: 'rgba(226,232,240,0.5)', type: 'solid' } }
            },
            series: [{
                name: '新增供应商',
                type: 'line',
                smooth: 0.4,
                showSymbol: true,
                symbol: 'circle',
                symbolSize: 6,
                itemStyle: { color: '#8b5cf6', borderWidth: 3, borderColor: '#fff' },
                lineStyle: { width: 4, shadowColor: 'rgba(139,92,246,0.4)', shadowBlur: 15, shadowOffsetY: 5 },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(139, 92, 246, 0.25)' },
                        { offset: 1, color: 'rgba(139, 92, 246, 0.01)' }
                    ])
                },
                label: {
                    show: true,
                    position: 'top',
                    distance: 10,
                    color: '#8b5cf6',
                    fontSize: 11,
                    fontWeight: 700,
                    fontFamily: DATA_FONT
                },
                data: [2, 2, 4, 3, 2]
            }]
        });
        chartInstances.supplier = chart;
    };

    // --- 4. 商品数量趋势 (V11 Pro Max) ---
    const initQuantity = () => {
        const el = document.getElementById('v11-quantity-chart');
        if (!el) return;
        const chart = echarts.init(el);
        chart.setOption({
            backgroundColor: 'transparent',
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'line', lineStyle: { color: '#cbd5e1', width: 2, type: 'dashed' } },
                ...TOOLTIP_STYLE,
                formatter: (params) => {
                    const p = params[0];
                    return `<div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#64748b;font-weight:700;margin-bottom:4px">${p.name}</div><div style="display:flex;align-items:center;gap:6px"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p.color}"></span><span style="font-family:${DATA_FONT};font-weight:800;font-size:14px;color:#0f172a">${p.value} 件</span></div>`;
                }
            },
            grid: { top: 30, left: 0, right: 10, bottom: 0, containLabel: true },
            xAxis: {
                type: 'category',
                boundaryGap: true,
                data: ['08月', '09月', '12月', '01月', '02月'],
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { ...LABEL_STYLE, margin: 16 }
            },
            yAxis: {
                type: 'value',
                axisLabel: { ...LABEL_STYLE, fontFamily: DATA_FONT, margin: 16 },
                splitLine: { lineStyle: { color: 'rgba(226,232,240,0.5)', type: 'solid' } }
            },
            series: [{
                name: '商品数量',
                type: 'bar',
                barWidth: '40%',
                itemStyle: { 
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#f59e0b' },
                        { offset: 1, color: '#d97706' }
                    ]), 
                    borderRadius: [4, 4, 0, 0],
                    shadowColor: 'rgba(245,158,11,0.2)',
                    shadowBlur: 10,
                    shadowOffsetY: 5
                },
                label: {
                    show: true,
                    position: 'top',
                    distance: 10,
                    color: '#f59e0b',
                    fontSize: 11,
                    fontWeight: 700,
                    fontFamily: DATA_FONT
                },
                data: [120, 150, 480, 2100, 1950]
            }]
        });
        chartInstances.quantity = chart;
    };

    // 初始化所有高端图表
    initTrend();
    initBreakdown();
    initSupplier();
    initQuantity();

    // 深度防抖 Resize 逻辑
    let resizeTimer = null;
    const handleResize = () => {
        if (resizeTimer) clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            Object.values(chartInstances).forEach(chart => {
                if (chart) chart.resize({ animation: { duration: 400, easing: 'cubicInOut' } });
            });
            console.log("Enterprise Analytics V11: Dimensions recalculation complete.");
        }, 150);
    };

    window.addEventListener('resize', handleResize);

    // 实时时钟 - 使用 Monospace 的数字格式
    const clockEl = document.getElementById('real-time-clock');
    if (clockEl) {
        setInterval(() => {
            const now = new Date();
            const timeStr = now.toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-');
            clockEl.innerText = timeStr;
        }, 1000);
    }

    // 添加入场动画 (Staggered Fade-in)
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 80));
    });

    // --- KPI 翻牌器动画 (Flip Counter) ---
    const animateCounters = () => {
        const counters = document.querySelectorAll('.kpi-counter');
        counters.forEach((counter) => {
            const target = parseFloat(counter.dataset.target);
            const decimals = parseInt(counter.dataset.decimals) || 0;
            const prefix = counter.dataset.prefix || '';
            const suffix = counter.dataset.suffix || '';
            const duration = 1500;
            const startTime = performance.now();

            const easeOutExpo = (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

            const update = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const easedProgress = easeOutExpo(progress);
                const current = easedProgress * target;
                const formatted = current.toLocaleString('en-US', { 
                    minimumFractionDigits: decimals, 
                    maximumFractionDigits: decimals 
                });
                counter.textContent = prefix + formatted + suffix;
                if (progress < 1) {
                    requestAnimationFrame(update);
                }
            };
            requestAnimationFrame(update);
        });
    };

    // 在入场动画完成后启动翻牌器
    setTimeout(animateCounters, 600);

    console.log("Enterprise Analytics V11: Pro Max Initialized.");
});
