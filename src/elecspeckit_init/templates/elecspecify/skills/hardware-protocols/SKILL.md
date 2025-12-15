---
name: hardware-protocols
description: 硬件通信协议专家支持,包括 MQTT, I2C, SPI, UART, BLE 和 WiFi。用于实现设备间通信、设计 MQTT 消息系统、配置总线协议、集成无线连接、排查协议问题或建立多设备嵌入式系统。特别适用于 IoT 项目、多外设嵌入式系统和分布式传感器网络。
requires_api: false
---

# Hardware Communication Protocols

## 概述

为嵌入式系统实现可靠的硬件通信协议。本 Skill 涵盖 MQTT (消息代理架构)、I2C/SPI (同步总线协议)、UART (串行通信)、BLE (低功耗蓝牙) 和 WiFi 网络。在设计微控制器、传感器、显示器和网络设备之间的通信时使用本 Skill。

## 何时使用本 Skill

在以下场景中调用本 Skill:
- 设置 MQTT broker 和客户端通信
- 设计主题层级和消息流
- 实现 I2C 传感器读取或设备控制
- 配置 SPI 显示或高速外设
- 建立 UART 与 AT 命令设备通信
- 创建 BLE GATT services 和 characteristics
- 集成 WiFi 连接和重连策略
- 排查协议时序或连接问题
- 构建多设备嵌入式系统

## 协议选择指南

根据需求选择合适的协议:

**MQTT** - 分布式系统的发布/订阅消息传递
- 使用场景: 多个设备需要同步状态更新
- 拓扑结构: 通过中央 broker 的多对多
- 传输范围: 取决于网络 (WiFi/Ethernet)
- 数据速率: 轻量级消息传递 (KB/s)
- 应用示例: 所有设备 ↔ Jetson broker 进行定时器同步、命令传递

**I2C** - 短距离外设的双线同步总线
- 使用场景: 共享总线上的多个低速传感器/设备
- 拓扑结构: 主/从模式 (单主机,多从机)
- 传输范围: PCB 板内 <1 米
- 数据速率: 100 KHz - 3.4 MHz
- 应用示例: 板载传感器 (温度、加速度计)

**SPI** - 高速外设的四线同步总线
- 使用场景: 需要快速显示、存储或传感器通信
- 拓扑结构: 主/从模式,独立片选信号
- 传输范围: PCB 板内 <1 米
- 数据速率: 高达 50+ MHz
- 应用示例: TFT 显示屏、SD 卡

**UART** - 点对点的异步串行通信
- 使用场景: 简单双向通信或 AT 命令
- 拓扑结构: 点对点 (一对一)
- 传输范围: 无 RS-232/RS-485 驱动器时 <15 米
- 数据速率: 典型 9600 - 115200+ baud
- 应用示例: 调试控制台、GPS 模块

**BLE** - 低功耗无线个人局域网
- 使用场景: 需要电池供电的无线通信
- 拓扑结构: 星型 (中心设备和外围设备)
- 传输范围: 室内约 10 米
- 数据速率: 约 1 Mbps (有效约 100 KB/s)
- 应用示例: 设备 ↔ 手机 App 进行通知传递

**WiFi** - 高速无线网络
- 使用场景: 需要互联网连接或高带宽本地网络
- 拓扑结构: 星型 (接入点和站点)
- 传输范围: 室内约 50 米
- 数据速率: 54 Mbps - 1+ Gbps
- 应用示例: 所有设备连接到家庭 WiFi 以访问 MQTT

## MQTT 实现

### Broker 设置

针对 Jetson Nano 或任何基于 Linux 的 MQTT broker,配置 Mosquitto 以同时支持 TCP (嵌入式设备) 和 WebSocket (Web 客户端)。

参考 `assets/mosquitto.conf` 中的配置模板并应用:

```bash
sudo cp assets/mosquitto.conf /etc/mosquitto/mosquitto.conf
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto
```

测试配置:

```bash
# 测试 TCP 监听器 (端口 1883)
mosquitto_pub -h localhost -t test/topic -m "hello"

# 测试 WebSocket 监听器 (端口 9001)
# 需要 mqtt.js 或类似的 WebSocket MQTT 客户端
node -e "const mqtt=require('mqtt'); const c=mqtt.connect('ws://localhost:9001'); c.on('connect',()=>{c.publish('test/topic','hello');c.end();})"
```

### 主题设计模式

设计主题层级结构以提高清晰度和可扩展性:

```
<project>/<category>/<action>/<target>

示例:
orbit/timer/state/current          - 当前定时器状态 (retained)
orbit/timer/control/start          - 启动定时器命令
orbit/timer/control/pause          - 暂停定时器命令
orbit/device/presto/status         - Presto 设备状态 (retained)
orbit/device/tembed/battery        - T-Embed 电池电量
orbit/alert/visual/all             - 向所有设备发送视觉警报
orbit/alert/visual/presto          - 向特定设备发送视觉警报
orbit/metrics/focus/1234567890     - 带时间戳的专注度指标
```

**主题命名约定:**
- 使用小写字母,用下划线或连字符分隔
- 结构层级化: 通用 → 特定
- 使用 `state` 表示当前值 (通常 retained)
- 使用 `control` 或 `command` 表示操作
- 在针对特定设备时包含设备 ID
- 为时间序列数据添加时间戳后缀

### QoS 级别选择

根据消息重要性选择服务质量级别:

**QoS 0 (At most once)** - 即发即弃
- 使用场景: 频繁的传感器更新、非关键状态
- 示例: `orbit/device/presto/rssi` (WiFi 信号强度)
- 权衡: 开销最低,可能丢失消息

**QoS 1 (At least once)** - 确认交付
- 使用场景: 命令、重要状态更改、定时器同步
- 示例: `orbit/timer/control/start`, `orbit/timer/state/current`
- 权衡: 保证交付,可能重复

**QoS 2 (Exactly once)** - 保证单次交付
- 使用场景: 关键命令,重复会导致问题的情况
- 示例: 支付交易、不可逆操作
- 权衡: 开销最高,交付最慢
- 注意: 很少需要; QoS 1 通常已足够

### Retained Messages 和 Last Will

使用 retained 消息保存新客户端立即需要的状态:

```python
# 发布 retained 消息 (状态持久保存在 broker 上)
client.publish("orbit/timer/state/current",
               json.dumps({"running": True, "remaining": 900}),
               qos=1,
               retain=True)

# 新客户端自动接收最后的 retained 消息
```

配置 Last Will and Testament 进行断连检测:

```python
# 连接时设置 LWT
client.will_set("orbit/device/presto/status",
                json.dumps({"online": False}),
                qos=1,
                retain=True)

# 正常连接时,发布在线状态
client.publish("orbit/device/presto/status",
               json.dumps({"online": True}),
               qos=1,
               retain=True)

# 如果连接丢失, broker 自动发布 LWT
```

### 连接和重连策略

实现具有指数退避的健壮重连机制。参考 `scripts/mqtt_connection.py` 获取完整实现。

关键原则:
1. **Clean Session vs Persistent Session**
   - Clean session (clean_start=True): 断连时丢弃订阅
   - Persistent session (clean_start=False): 维护订阅并缓存 QoS 1/2 消息
   - 建议: 设备使用 persistent sessions,短期客户端使用 clean

2. **Keep-Alive 间隔**
   - 稳定网络设置为 60 秒
   - 不可靠 WiFi 设置为 30 秒
   - 必须在间隔到期前发送 PING 以维持连接

3. **自动重连**
   - 实现指数退避: 1s, 2s, 4s, 8s... 最多 60s
   - 成功连接时重置退避计时器
   - 断连期间在本地缓存消息 (带大小限制)

4. **连接状态处理**
   - 实现连接回调: on_connect, on_disconnect
   - 在 on_connect 回调中重新订阅主题
   - 更新 UI/LED 显示连接状态
   - 记录连接事件以便调试

## I2C 协议

### 主机配置

在 ESP32 或 RP2350 上配置 I2C 主机:

```cpp
// ESP-IDF 示例
#include "driver/i2c.h"

#define I2C_MASTER_SCL_IO    22      // SCL 的 GPIO
#define I2C_MASTER_SDA_IO    21      // SDA 的 GPIO
#define I2C_MASTER_FREQ_HZ   100000  // 100 KHz 标准模式

i2c_config_t conf = {
    .mode = I2C_MODE_MASTER,
    .sda_io_num = I2C_MASTER_SDA_IO,
    .scl_io_num = I2C_MASTER_SCL_IO,
    .sda_pullup_en = GPIO_PULLUP_ENABLE,
    .scl_pullup_en = GPIO_PULLUP_ENABLE,
    .master.clk_speed = I2C_MASTER_FREQ_HZ,
};

i2c_param_config(I2C_NUM_0, &conf);
i2c_driver_install(I2C_NUM_0, conf.mode, 0, 0, 0);
```

**上拉电阻**: I2C 运行所必需
- 典型值: 2.2 KΩ - 10 KΩ
- 较低值 (2.2 KΩ) 用于较长走线或较高电容
- 较高值 (10 KΩ) 用于较慢速度或节能
- 许多开发板包含板载上拉电阻

### 设备地址

I2C 使用 7 位寻址 (128 个可能地址):

```
常见 I2C 地址:
0x68 - MPU-6050 (加速度计/陀螺仪)
0x76 or 0x77 - BMP280 (气压/温度)
0x3C or 0x3D - SSD1306 (OLED 显示)
0x48-0x4F - ADS1115 (ADC)

特殊地址:
0x00 - 通用呼叫地址
0x01-0x07 - 保留
0x78-0x7F - 保留
```

扫描总线上的设备:

```cpp
for (uint8_t addr = 1; addr < 127; addr++) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, 50 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    if (ret == ESP_OK) {
        printf("Found device at 0x%02X\n", addr);
    }
}
```

### 读取传感器

参考 `scripts/i2c_sensor.py` 中的实现,演示了带有正确错误处理的 I2C 传感器读取。

基本 I2C 读取事务:

```cpp
esp_err_t i2c_read_sensor(uint8_t device_addr, uint8_t reg_addr,
                          uint8_t* data, size_t len) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();

    // 写寄存器地址
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (device_addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, reg_addr, true);

    // 读数据
    i2c_master_start(cmd);  // 重复起始
    i2c_master_write_byte(cmd, (device_addr << 1) | I2C_MASTER_READ, true);
    i2c_master_read(cmd, data, len, I2C_MASTER_LAST_NACK);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    return ret;
}
```

**错误处理:**
- 检查返回值以查找超时或 NACK
- 对瞬态故障使用指数退避重试
- 对持久故障重置总线
- 记录错误及上下文 (地址、寄存器、数据)

## SPI 协议

### 主机配置

为显示器或高速外设配置 SPI 主机:

```cpp
// ESP-IDF SPI 显示示例
#include "driver/spi_master.h"

#define PIN_MOSI  23
#define PIN_CLK   18
#define PIN_CS    5
#define PIN_DC    17  // Data/Command 选择
#define PIN_RST   16  // 复位

spi_bus_config_t bus_cfg = {
    .mosi_io_num = PIN_MOSI,
    .miso_io_num = -1,  // 显示器不使用
    .sclk_io_num = PIN_CLK,
    .quadwp_io_num = -1,
    .quadhd_io_num = -1,
    .max_transfer_sz = 320 * 240 * 2 + 8,  // 显示缓冲区大小
};

spi_device_interface_config_t dev_cfg = {
    .clock_speed_hz = 40 * 1000 * 1000,  // 40 MHz
    .mode = 0,  // SPI mode 0 (CPOL=0, CPHA=0)
    .spics_io_num = PIN_CS,
    .queue_size = 7,
    .pre_cb = nullptr,  // 传输前回调
};

spi_bus_initialize(SPI2_HOST, &bus_cfg, SPI_DMA_CH_AUTO);
spi_bus_add_device(SPI2_HOST, &dev_cfg, &spi_handle);
```

### SPI 模式 (CPOL 和 CPHA)

SPI 根据时钟极性和相位有四种模式:

```
Mode | CPOL | CPHA | 描述
-----|------|------|--------------------------------------------------
0    | 0    | 0    | 上升沿采样数据,下降沿移位
1    | 0    | 1    | 下降沿采样数据,上升沿移位
2    | 1    | 0    | 下降沿采样数据,上升沿移位
3    | 1    | 1    | 上升沿采样数据,下降沿移位

常见设备:
- 大多数显示器: Mode 0 或 Mode 3
- SD 卡: Mode 0
- MAX31855 热电偶: Mode 0
```

在数据手册中验证正确模式 - 使用错误模式会导致数据乱码。

### DMA 传输

使用 DMA 进行大数据传输以减少 CPU 负载:

```cpp
// 准备事务
spi_transaction_t trans = {
    .length = buffer_size * 8,  // 长度以位为单位
    .tx_buffer = buffer,
    .rx_buffer = nullptr,
};

// 非阻塞 DMA 传输
spi_device_queue_trans(spi_handle, &trans, portMAX_DELAY);

// 传输期间进行其他工作...

// 等待完成
spi_transaction_t* ret_trans;
spi_device_get_trans_result(spi_handle, &ret_trans, portMAX_DELAY);
```

**性能考虑:**
- 对 >64 字节的传输使用 DMA
- 对 DMA 将缓冲区对齐到 4 字节边界
- 排队多个事务以保持总线繁忙
- 考虑双缓冲以实现连续更新

参考 `scripts/spi_display.py` 获取完整的 SPI 显示驱动示例。

## UART 协议

### 配置

使用正确的帧格式配置 UART:

```cpp
// ESP-IDF 示例
#include "driver/uart.h"

#define UART_NUM      UART_NUM_1
#define TXD_PIN       17
#define RXD_PIN       16
#define BAUD_RATE     115200

uart_config_t uart_config = {
    .baud_rate = BAUD_RATE,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
};

uart_param_config(UART_NUM, &uart_config);
uart_set_pin(UART_NUM, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
uart_driver_install(UART_NUM, 1024, 1024, 0, NULL, 0);
```

**流控制:**
- 无: 简单点对点,确保接收器能够跟上
- 软件 (XON/XOFF): 硬件流控不可用时使用
- 硬件 (RTS/CTS): 可靠高速通信的首选

### AT 命令接口

许多模块 (WiFi, BLE, GPS) 使用 AT 命令接口。参考 `scripts/uart_parser.py` 获取带状态机的完整命令解析器。

基本 AT 命令处理:

```cpp
void send_at_command(const char* cmd, char* response, size_t max_len) {
    // 发送命令,附带 CR+LF
    uart_write_bytes(UART_NUM, cmd, strlen(cmd));
    uart_write_bytes(UART_NUM, "\r\n", 2);

    // 带超时读取响应
    int len = uart_read_bytes(UART_NUM, (uint8_t*)response,
                              max_len - 1, 1000 / portTICK_PERIOD_MS);
    response[len] = '\0';

    // 检查 OK/ERROR
    if (strstr(response, "OK")) {
        // 成功
    } else if (strstr(response, "ERROR")) {
        // 失败
    }
}
```

**AT 命令最佳实践:**
- 在发送下一条命令前等待 "OK"
- 为每条命令实现超时
- 处理非请求响应 (事件)
- 缓冲部分行,直到收到 CR+LF
- 对复杂命令序列使用状态机

## BLE 协议

### GATT Server 结构

为每种数据类型设计包含 characteristics 的 GATT services:

```
Service: Timer Control (UUID: custom)
├── Characteristic: State (UUID: 0x2A00)
│   ├── Properties: Read, Notify
│   ├── Value: {"running": bool, "remaining": uint32}
│   └── Descriptor: CCCD (0x2902) for notifications
├── Characteristic: Command (UUID: 0x2A01)
│   ├── Properties: Write
│   └── Value: {"action": "start"|"pause"|"reset", "duration": uint32}
└── Characteristic: Battery (UUID: 0x2A19)
    ├── Properties: Read, Notify
    └── Value: uint8 (percentage)
```

### 连接参数

根据使用场景优化连接间隔:

```cpp
// 快速更新 (定时器显示): 20ms - 40ms 间隔
// 节能 (空闲): 200ms - 400ms 间隔

ble_gap_conn_params_t conn_params = {
    .min_conn_interval = 16,  // 16 * 1.25ms = 20ms
    .max_conn_interval = 32,  // 32 * 1.25ms = 40ms
    .slave_latency = 0,       // 实时更新无延迟
    .conn_sup_timeout = 400,  // 400 * 10ms = 4s 超时
};
```

**权衡:**
- 更快间隔: 更低延迟,更高功耗
- 更慢间隔: 更长延迟,更好的电池寿命
- Slave latency: 跳过 N 个间隔以节能 (增加延迟)

### Notifications vs Indications

选择适当的 characteristic 属性:

**Notifications** (未确认)
- 使用场景: 频繁的传感器更新、定时器滴答
- 优点: 较低开销,较高吞吐量
- 缺点: 无交付保证

**Indications** (已确认)
- 使用场景: 重要命令、关键状态更改
- 优点: 保证交付并确认
- 缺点: 较高开销,较低吞吐量

参考 `scripts/ble_gatt_server.py` 获取完整的 BLE GATT server 实现。

## WiFi 集成

### 连接管理

实现具有自动重连的健壮 WiFi 连接:

```cpp
// ESP-IDF 示例
void wifi_init() {
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);

    esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL);
    esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL);

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };

    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();
}

void event_handler(void* arg, esp_event_base_t event_base,
                   int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        esp_wifi_connect();  // 自动重连
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        // 已连接 - 启动 MQTT 客户端
    }
}
```

### mDNS 服务发现

使用 mDNS 发现 MQTT broker,无需硬编码 IP:

```cpp
// 发布 MQTT broker (Jetson)
mdns_init();
mdns_hostname_set("orbit-broker");
mdns_service_add("Orbit MQTT", "_mqtt", "_tcp", 1883, NULL, 0);

// 发现 MQTT broker (设备)
mdns_result_t* results = NULL;
esp_err_t err = mdns_query_ptr("_mqtt", "_tcp", 3000, 20, &results);

if (err == ESP_OK && results) {
    mdns_result_t* r = results;
    while (r) {
        printf("Found MQTT broker: %s at %s:%d\n",
               r->hostname, ip4addr_ntoa(&r->addr->addr.u_addr.ip4), r->port);
        r = r->next;
    }
    mdns_query_results_free(results);
}
```

## 故障排除

### MQTT 问题

**连接被拒:**
- 检查防火墙: `sudo ufw allow 1883` 和 `sudo ufw allow 9001`
- 验证 broker 运行: `sudo systemctl status mosquitto`
- 检查日志: `sudo journalctl -u mosquitto -f`

**消息未收到:**
- 验证主题拼写 (区分大小写)
- 检查 QoS 级别和订阅
- 监控所有主题: `mosquitto_sub -h localhost -t '#' -v`

**WebSocket 连接失败:**
- 验证 mosquitto.conf 中的 WebSocket 监听器
- 测试: `wscat -c ws://broker-ip:9001/mqtt`
- 如果从浏览器访问,检查 CORS

### I2C 问题

**设备未检测到:**
- 检查接线: SDA/SCL 未交换
- 验证存在上拉电阻 (2.2K - 10K)
- 扫描总线: 使用上面的 I2C 扫描器代码
- 检查数据手册中的设备地址 (有些有可配置位)

**超时或 NACK:**
- 降低时钟速度 (尝试 100 KHz)
- 检查设备供电
- 验证设备就绪 (有些需要初始化延迟)
- 检查总线争用 (多主机)

### SPI 问题

**数据乱码:**
- 验证 SPI 模式 (CPOL/CPHA)
- 检查时钟速度 (尝试更慢)
- 确认 MISO/MOSI 未交换
- 验证 CS 时序 (某些设备需要延迟)

**无响应:**
- 检查片选 (通常低电平有效)
- 验证设备供电
- 用逻辑分析仪检查 MOSI/CLK 信号
- 某些设备需要初始化序列

### BLE 问题

**连接断开:**
- 增加连接超时
- 减少连接间隔
- 检查 RF 干扰
- 验证电源供应稳定

**无法发现设备:**
- 检查广播间隔和窗口
- 验证设备名称/UUID
- 检查 iOS/Android BLE 权限
- 扫描更长时间或重启蓝牙

### WiFi 问题

**无法连接:**
- 验证 SSID 和密码
- 检查 WiFi 频段 (2.4 GHz vs 5 GHz)
- 如果 DHCP 失败,尝试静态 IP
- 检查路由器防火墙/MAC 过滤

**频繁断连:**
- 减少 WiFi 节能
- 改善信号强度 (更靠近 AP)
- 检查信道拥塞
- 使用 WiFi 分析器寻找更好的信道

## ElecSpeckit 集成指南

### 在 ElecSpeckit 工作流中使用本 Skill

本 Skill 在 ElecSpeckit 硬件设计工作流的多个阶段发挥关键作用:

#### 1. 架构设计阶段 (/elecspeckit.plan)

**场景**: 规划嵌入式系统的通信架构

**使用方式**:
```
用户: /elecspeckit.plan
AI: 我们正在规划通信架构。让我调用 hardware-protocols Skill 来帮助选择合适的协议...

[分析需求]
- 设备数量: 5 个 (主控 + 4 个传感器模块)
- 传输距离: PCB 板内短距离 + 无线手机连接
- 数据速率: 传感器数据 <1KB/s, 显示更新需要高速

[推荐方案]
1. 主控 ↔ 传感器: I2C (共享总线, 100 KHz 足够)
2. 主控 ↔ 显示: SPI (高速刷新, 40 MHz)
3. 主控 ↔ 手机: BLE (低功耗无线)
4. 系统间同步: MQTT (如果有 WiFi 模块)
```

**输出**: 在 `plan.md` 中生成通信架构设计方案,包含协议选型理由和关键参数

#### 2. 规格编写阶段 (/elecspeckit.specify)

**场景**: 编写通信接口的详细技术规格

**使用方式**:
```
用户: /elecspeckit.specify
AI: 我将为 I2C 接口编写详细规格...

[调用 hardware-protocols Skill]
根据协议选择指南和 I2C 章节内容:

## 3.2 I2C 接口规格

### 电气特性
- 时钟频率: 100 KHz (标准模式)
- 电压电平: 3.3V
- 上拉电阻: 4.7 KΩ (板载)

### 设备地址分配
- 温度传感器 (BMP280): 0x76
- 加速度计 (MPU6050): 0x68
- EEPROM (AT24C32): 0x50

### 通信时序
- 启动延迟: ≥ 100ms (等待传感器上电)
- 读取超时: 1000ms
- 重试策略: 指数退避, 最多 3 次
```

**输出**: 在 `spec.md` 中生成详细的接口规格说明,符合 IEEE 标准

#### 3. 固件开发和调试阶段

**场景**: 实现通信协议代码并排查问题

**使用方式**:
```
用户: 我的 SPI 显示一直显示乱码,怎么办?

AI: [调用 hardware-protocols Skill - SPI 故障排除部分]

根据 "SPI 问题 - 数据乱码" 章节:

可能原因:
1. SPI 模式不匹配 - 检查 CPOL/CPHA 配置
2. 时钟速度过快 - 尝试降低到 10 MHz
3. MISO/MOSI 引脚接反

请尝试以下代码修改:
[提供正确的 spi_device_interface_config_t 配置]

参考本项目的 `scripts/spi_display.py` 查看完整示例。
```

**输出**: 提供针对性的调试建议和代码示例

#### 4. 系统集成和测试阶段

**场景**: 验证多协议协同工作

**使用方式**:
```
用户: 如何测试 MQTT + I2C + SPI 的集成系统?

AI: [调用 hardware-protocols Skill - 集成测试部分]

测试方案:
1. 独立测试每个协议
   - I2C: 运行设备扫描,验证所有地址
   - SPI: 显示测试图案
   - MQTT: 发布/订阅测试主题

2. 集成测试流程
   [提供基于 Orbit 系统的测试脚本示例]
   - I2C 读传感器 → MQTT 发布 → SPI 显示

3. 性能监控
   - 消息延迟: MQTT QoS 1, <100ms
   - I2C 错误率: <0.1%
   - SPI 帧率: ≥30 FPS
```

### 与其他 ElecSpeckit Skills 协同

本 Skill 经常与以下 Skills 配合使用:

- **embedded-systems**: 提供 RTOS 任务管理,与本 Skill 的协议实现结合
- **esp32-embedded-dev**: ESP32 平台特定的协议实现细节
- **embedded-best-practices**: 代码规范和错误处理策略
- **docs-write**: 生成协议接口文档和数据手册

### 配置建议

在 `.elecspecify/memory/skill_config.json` 中:
```json
{
  "hardware-protocols": {
    "enabled": true,
    "requires_api": false,
    "priority": "high"
  }
}
```

建议在以下项目类型中**默认启用**:
- IoT 设备开发
- 多传感器嵌入式系统
- 无线通信产品
- 显示类硬件产品

## 附带资源

### scripts/

可执行的参考实现:
- `mqtt_connection.py` - 带健壮重连逻辑的 MQTT 客户端
- `ble_gatt_server.py` - 带 services 和 characteristics 的 BLE GATT server
- `i2c_sensor.py` - 带错误处理的 I2C 传感器读取
- `spi_display.py` - 带 DMA 的 SPI 显示驱动
- `uart_parser.py` - 带状态机的 UART 命令解析器

这些脚本可以直接执行或适配到特定硬件平台。

### references/

详细协议文档:
- `mqtt_reference.md` - 完整的 MQTT 协议规范和模式
- `embedded_bus_protocols.md` - I2C, SPI, UART 详细规格
- `wireless_protocols.md` - BLE 和 WiFi 综合指南
- `orbit_integration.md` - Orbit 特定的集成模式和主题架构

当需要深入协议知识时加载这些参考资料。

### assets/

配置模板:
- `mosquitto.conf` - 生产就绪的 Mosquitto 配置 (TCP + WebSocket)
- `platformio_examples/` - ESP32 和 RP2350 的 PlatformIO 项目配置

将这些模板复制到项目中并根据需要自定义。

---

**版本**: v0.2.0
**维护者**: ElecSpeckit Team
**许可证**: Apache License 2.0
