---
name: architecture-diagrams
description: 使用 Mermaid、PlantUML、C4 模型、流程图和序列图创建系统架构图。在记录架构、系统设计、数据流或技术工作流时使用。
---
# Architecture Diagrams (架构图)

使用 Mermaid、PlantUML、C4 模型、流程图和时序图创建系统架构图。

## 概述

使用基于代码的图表工具（如 Mermaid 和 PlantUML）创建清晰、可维护的架构图，用于系统设计、数据流和技术文档。

## 何时使用

- 系统架构文档
- C4 模型图
- 数据流图
- 时序图
- 组件关系图
- 部署图
- 基础设施架构
- 微服务架构
- 数据库模式（可视化）
- 集成模式
- 嵌入式系统硬件架构
- 电路模块交互关系
- 通信协议流程
- 状态机设计

## 工具选择指南

### Mermaid

**优势**：

- GitHub/GitLab 原生支持
- 语法简洁，易于学习
- 适合快速原型
- 支持实时预览

**适用场景**：

- 系统架构图
- 流程图
- 时序图
- 甘特图
- 类图（简单场景）
- 状态图
- ER 图

**示例**：

```mermaid
graph LR
    A[客户端] --> B[API 网关]
    B --> C[服务层]
    C --> D[数据库]
```

### PlantUML

**优势**：

- 功能强大，支持复杂图表
- 适合详细的类图和组件图
- 丰富的样式选项
- 支持多种导出格式

**适用场景**：

- UML 类图
- 详细的组件图
- 部署图
- 用例图
- 活动图
- 对象图

**示例**：

```plantuml
@startuml
class MCU {
  +init()
  +sleep()
}
@enduml
```

### C4 模型

**优势**：

- 分层次的架构视图
- 适合大型系统
- 清晰的抽象级别
- 便于不同受众理解

**层次**：

1. **Context（上下文）**：系统与外部实体的关系
2. **Container（容器）**：系统内的高层技术构件
3. **Component（组件）**：容器内的组件
4. **Code（代码）**：类和方法（可选）

## Mermaid 详细示例

### 1. 系统架构图

```mermaid
graph TB
    subgraph "客户端层"
        Web[Web 应用]
        Mobile[移动应用]
        CLI[CLI 工具]
    end

    subgraph "API 网关层"
        Gateway[API 网关<br/>限流<br/>认证]
    end

    subgraph "服务层"
        Auth[认证服务]
        User[用户服务]
        Order[订单服务]
        Payment[支付服务]
        Notification[通知服务]
    end

    subgraph "数据层"
        UserDB[(用户数据库<br/>PostgreSQL)]
        OrderDB[(订单数据库<br/>PostgreSQL)]
        Cache[(Redis 缓存)]
        Queue[消息队列<br/>RabbitMQ]
    end

    subgraph "外部服务"
        Stripe[Stripe API]
        SendGrid[SendGrid]
        S3[AWS S3]
    end

    Web --> Gateway
    Mobile --> Gateway
    CLI --> Gateway

    Gateway --> Auth
    Gateway --> User
    Gateway --> Order
    Gateway --> Payment

    Auth --> UserDB
    User --> UserDB
    User --> Cache
    Order --> OrderDB
    Order --> Queue
    Payment --> Stripe
    Queue --> Notification
    Notification --> SendGrid

    Order --> S3
    User --> S3

    style Gateway fill:#ff6b6b
    style Auth fill:#4ecdc4
    style User fill:#4ecdc4
    style Order fill:#4ecdc4
    style Payment fill:#4ecdc4
    style Notification fill:#4ecdc4
```

### 2. 时序图

```mermaid
sequenceDiagram
    actor User as 用户
    participant Web as Web 应用
    participant Gateway as API 网关
    participant Auth as 认证服务
    participant Order as 订单服务
    participant Payment as 支付服务
    participant DB as 数据库
    participant Queue as 消息队列
    participant Email as 邮件服务

    User->>Web: 下单
    Web->>Gateway: POST /orders
    Gateway->>Auth: 验证令牌
    Auth-->>Gateway: 令牌有效

    Gateway->>Order: 创建订单
    Order->>DB: 保存订单
    DB-->>Order: 订单已保存
    Order->>Payment: 处理支付
    Payment->>Payment: 扣款
    Payment-->>Order: 支付成功
    Order->>Queue: 发布订单事件
    Queue->>Email: 发送确认邮件
    Email->>User: 订单确认

    Order-->>Gateway: 订单已创建
    Gateway-->>Web: 201 Created
    Web-->>User: 订单成功

    Note over User,Email: 通过队列异步发送邮件
```

### 3. C4 上下文图

```mermaid
graph TB
    subgraph "电商系统"
        System[电商平台<br/>管理产品、订单<br/>和客户账户]
    end

    Customer[客户<br/>浏览和购买产品]
    Admin[管理员<br/>管理产品和订单]

    Email[邮件系统<br/>SendGrid]
    Payment[支付提供商<br/>Stripe]
    Analytics[分析平台<br/>Google Analytics]

    Customer -->|浏览, 下单| System
    Admin -->|管理| System
    System -->|发送邮件| Email
    System -->|处理支付| Payment
    System -->|跟踪事件| Analytics

    style System fill:#1168bd
    style Customer fill:#08427b
    style Admin fill:#08427b
    style Email fill:#999
    style Payment fill:#999
    style Analytics fill:#999
```

### 4. 组件图

```mermaid
graph LR
    subgraph "前端"
        UI[React UI]
        Store[Redux Store]
        Router[React Router]
    end

    subgraph "API 层"
        REST[REST API]
        WS[WebSocket]
        GQL[GraphQL]
    end

    subgraph "业务逻辑"
        ProductSvc[产品服务]
        OrderSvc[订单服务]
        AuthSvc[认证服务]
    end

    subgraph "数据访问"
        ProductRepo[产品仓储]
        OrderRepo[订单仓储]
        UserRepo[用户仓储]
        Cache[缓存层]
    end

    subgraph "基础设施"
        DB[(PostgreSQL)]
        Redis[(Redis)]
        S3[AWS S3]
    end

    UI --> Store
    Store --> Router
    UI --> REST
    UI --> WS
    UI --> GQL

    REST --> ProductSvc
    REST --> OrderSvc
    REST --> AuthSvc
    WS --> OrderSvc
    GQL --> ProductSvc

    ProductSvc --> ProductRepo
    OrderSvc --> OrderRepo
    AuthSvc --> UserRepo

    ProductRepo --> DB
    OrderRepo --> DB
    UserRepo --> DB
    ProductRepo --> Cache
    Cache --> Redis
    ProductSvc --> S3
```

### 5. 部署图

```mermaid
graph TB
    subgraph "AWS 云"
        subgraph "VPC"
            subgraph "公有子网"
                ALB[应用<br/>负载均衡器]
                NAT[NAT 网关]
            end

            subgraph "私有子网 1"
                ECS1[ECS 容器<br/>服务实例 1]
                ECS2[ECS 容器<br/>服务实例 2]
            end

            subgraph "私有子网 2"
                RDS1[(RDS 主库)]
                RDS2[(RDS 副本)]
            end

            subgraph "私有子网 3"
                ElastiCache[(ElastiCache<br/>Redis 集群)]
            end
        end

        Route53[Route 53<br/>DNS]
        CloudFront[CloudFront CDN]
        S3[S3 存储桶<br/>静态资源]
        ECR[ECR<br/>容器注册表]
    end

    Users[用户] --> Route53
    Route53 --> CloudFront
    CloudFront --> ALB
    CloudFront --> S3
    ALB --> ECS1
    ALB --> ECS2
    ECS1 --> RDS1
    ECS2 --> RDS1
    RDS1 --> RDS2
    ECS1 --> ElastiCache
    ECS2 --> ElastiCache
    ECS1 --> S3
    ECS2 --> S3
    ECS1 -.拉取镜像.-> ECR
    ECS2 -.拉取镜像.-> ECR

    style ALB fill:#ff6b6b
    style ECS1 fill:#4ecdc4
    style ECS2 fill:#4ecdc4
    style RDS1 fill:#95e1d3
    style RDS2 fill:#95e1d3
```

### 6. 数据流图

```mermaid
graph LR
    User[用户操作] --> Frontend[前端应用]
    Frontend --> Validation{验证}
    Validation -->|无效| Error[显示错误]
    Validation -->|有效| API[API 请求]
    API --> Auth{已认证?}
    Auth -->|否| Unauthorized[401 响应]
    Auth -->|是| Service[业务服务]
    Service --> Database[(数据库)]
    Service --> Cache[(缓存)]
    Cache -->|命中| Return[返回缓存]
    Cache -->|未命中| Database
    Database --> Transform[转换数据]
    Transform --> Response[API 响应]
    Response --> Frontend
    Frontend --> Render[渲染 UI]
```

### 7. 嵌入式系统架构图

```mermaid
graph TB
    subgraph "传感器层"
        Temp[温度传感器<br/>DS18B20]
        Humid[湿度传感器<br/>DHT22]
        Motion[运动传感器<br/>PIR]
    end

    subgraph "微控制器"
        MCU[ESP32<br/>主控芯片]
        ADC[ADC 模块]
        GPIO[GPIO 模块]
        UART[UART 模块]
        SPI[SPI 模块]
        I2C[I2C 模块]
    end

    subgraph "通信模块"
        WiFi[WiFi 模块]
        BLE[蓝牙 BLE]
    end

    subgraph "执行器"
        Motor[电机驱动<br/>L298N]
        Relay[继电器]
        LED[状态指示灯]
    end

    subgraph "电源管理"
        Battery[锂电池<br/>3.7V]
        Charger[充电管理<br/>TP4056]
        Regulator[稳压器<br/>AMS1117-3.3]
    end

    Temp --> I2C
    Humid --> GPIO
    Motion --> GPIO
    I2C --> MCU
    GPIO --> MCU
    MCU --> WiFi
    MCU --> BLE
    MCU --> Motor
    MCU --> Relay
    MCU --> LED
    Battery --> Charger
    Charger --> Regulator
    Regulator --> MCU

    style MCU fill:#ff6b6b
    style WiFi fill:#4ecdc4
    style BLE fill:#4ecdc4
```

### 8. 通信协议时序图

```mermaid
sequenceDiagram
    participant MCU as 微控制器
    participant Sensor as I2C 传感器
    participant Module as WiFi 模块
    participant Server as 云服务器

    MCU->>Sensor: START + 地址 (0x48)
    Sensor-->>MCU: ACK
    MCU->>Sensor: 写入命令 (0x01)
    Sensor-->>MCU: ACK
    MCU->>Sensor: STOP

    Note over MCU,Sensor: 等待转换完成 (100ms)

    MCU->>Sensor: START + 地址 (0x48)
    Sensor-->>MCU: ACK
    MCU->>Sensor: 读取请求
    Sensor-->>MCU: 数据字节 1
    MCU-->>Sensor: ACK
    Sensor-->>MCU: 数据字节 2
    MCU-->>Sensor: NACK
    MCU->>Sensor: STOP

    MCU->>Module: AT+CIPSTART="TCP","server.com",80
    Module-->>MCU: CONNECT OK
    MCU->>Module: AT+CIPSEND=50
    Module-->>MCU: >
    MCU->>Module: POST /api/data HTTP/1.1...
    Module->>Server: HTTP 请求
    Server-->>Module: HTTP 响应
    Module-->>MCU: +IPD,100:{"status":"ok"}
```

### 9. 状态机图

```mermaid
stateDiagram-v2
    [*] --> 空闲
    空闲 --> 初始化: 上电
    初始化 --> 连接WiFi: 初始化完成
    连接WiFi --> 已连接: WiFi 连接成功
    连接WiFi --> 错误: WiFi 连接失败
    已连接 --> 采集数据: 定时器触发
    采集数据 --> 数据处理: 数据采集完成
    数据处理 --> 发送数据: 处理完成
    发送数据 --> 已连接: 发送成功
    发送数据 --> 错误: 发送失败
    错误 --> 连接WiFi: 重试
    错误 --> 睡眠模式: 超过最大重试次数
    睡眠模式 --> 空闲: 唤醒定时器
    已连接 --> 睡眠模式: 无活动超时
```

## PlantUML 详细示例

### 1. 类图

```plantuml
@startuml
class Order {
  -id: UUID
  -customerId: UUID
  -items: OrderItem[]
  -status: OrderStatus
  -totalAmount: number
  -createdAt: Date
  +calculateTotal(): number
  +addItem(item: OrderItem): void
  +removeItem(itemId: UUID): void
  +updateStatus(status: OrderStatus): void
}

class OrderItem {
  -id: UUID
  -productId: UUID
  -quantity: number
  -price: number
  +getSubtotal(): number
}

class Customer {
  -id: UUID
  -name: string
  -email: string
  -orders: Order[]
  +placeOrder(order: Order): void
  +getOrderHistory(): Order[]
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

Customer "1" -- "*" Order: 下单
Order "1" *-- "*" OrderItem: 包含
Order -- OrderStatus: 拥有
@enduml
```

### 2. 组件图

```plantuml
@startuml
package "前端" {
  [Web 应用]
  [移动应用]
}

package "API 网关" {
  [负载均衡器]
  [API 网关]
}

package "微服务" {
  [用户服务]
  [产品服务]
  [订单服务]
  [支付服务]
}

package "数据存储" {
  database "PostgreSQL" {
    [用户数据库]
    [产品数据库]
    [订单数据库]
  }
  database "Redis" {
    [缓存]
    [会话存储]
  }
}

[Web 应用] --> [负载均衡器]
[移动应用] --> [负载均衡器]
[负载均衡器] --> [API 网关]
[API 网关] --> [用户服务]
[API 网关] --> [产品服务]
[API 网关] --> [订单服务]
[API 网关] --> [支付服务]

[用户服务] --> [用户数据库]
[产品服务] --> [产品数据库]
[订单服务] --> [订单数据库]
[用户服务] --> [缓存]
[产品服务] --> [缓存]
[API 网关] --> [会话存储]
@enduml
```

### 3. 部署图

```plantuml
@startuml
node "CDN (CloudFront)" {
  [静态资源]
}

node "负载均衡器" {
  [ALB]
}

node "应用服务器" {
  node "服务器 1" {
    [应用实例 1]
  }
  node "服务器 2" {
    [应用实例 2]
  }
}

node "数据库集群" {
  database "主库" {
    [PostgreSQL 主库]
  }
  database "副本" {
    [PostgreSQL 副本]
  }
}

node "缓存集群" {
  [Redis 主节点]
  [Redis 从节点]
}

[浏览器] --> [静态资源]
[浏览器] --> [ALB]
[ALB] --> [应用实例 1]
[ALB] --> [应用实例 2]
[应用实例 1] --> [PostgreSQL 主库]
[应用实例 2] --> [PostgreSQL 主库]
[PostgreSQL 主库] ..> [PostgreSQL 副本]: 复制
[应用实例 1] --> [Redis 主节点]
[应用实例 2] --> [Redis 主节点]
[Redis 主节点] ..> [Redis 从节点]: 复制
@enduml
```

### 4. 嵌入式系统类图

```plantuml
@startuml
class MCU {
  -clockSpeed: uint32_t
  -powerMode: PowerMode
  +init(): void
  +sleep(): void
  +wakeup(): void
  +setClockSpeed(speed: uint32_t): void
}

class Sensor {
  -address: uint8_t
  -sampleRate: uint16_t
  +read(): SensorData
  +calibrate(): void
  +reset(): void
}

class TemperatureSensor {
  -resolution: uint8_t
  +getTemperature(): float
  +setResolution(bits: uint8_t): void
}

class HumiditySensor {
  -compensationEnabled: bool
  +getHumidity(): float
  +enableCompensation(): void
}

class CommunicationModule {
  -baudRate: uint32_t
  -protocol: Protocol
  +connect(): bool
  +disconnect(): void
  +send(data: uint8_t[]): bool
  +receive(): uint8_t[]
}

class WiFiModule {
  -ssid: string
  -password: string
  +connectToAP(ssid: string, pass: string): bool
  +getSignalStrength(): int8_t
}

class BLEModule {
  -deviceName: string
  -advertisingInterval: uint16_t
  +startAdvertising(): void
  +stopAdvertising(): void
}

enum PowerMode {
  ACTIVE
  SLEEP
  DEEP_SLEEP
  STANDBY
}

MCU "1" -- "*" Sensor: 控制
MCU "1" -- "1" CommunicationModule: 使用
Sensor <|-- TemperatureSensor
Sensor <|-- HumiditySensor
CommunicationModule <|-- WiFiModule
CommunicationModule <|-- BLEModule
MCU -- PowerMode
@enduml
```

## 最佳实践

### 通用原则

1. **保持简洁**

   - 每个图表只关注一个方面
   - 避免在单个图表中混合多个抽象级别
   - 使用子图对相关元素进行分组
2. **一致性**

   - 在整个项目中使用一致的符号
   - 保持命名约定的一致性
   - 使用统一的颜色方案
3. **可读性**

   - 使用清晰的标签和描述
   - 添加图例说明复杂的符号
   - 使用颜色编码传达含义
   - 确保文本大小适当
4. **可维护性**

   - 使用基于文本的格式（Mermaid、PlantUML）
   - 将图表与代码一起版本控制
   - 定期更新图表以反映代码更改
   - 添加注释说明设计决策

### 针对嵌入式系统的建议

1. **硬件架构图**

   - 清晰标注通信接口（I2C、SPI、UART等）
   - 标明电压等级和功耗信息
   - 显示关键的时序关系
   - 包含引脚分配信息
2. **通信协议图**

   - 使用时序图展示协议交互
   - 标注时间约束和延迟
   - 显示错误处理流程
   - 包含重试机制
3. **状态机设计**

   - 明确标注所有状态转换条件
   - 包含超时和错误状态
   - 标明入口和出口动作
   - 考虑所有边界情况

### ✅ 应该做的

- 使用一致的符号和记号
- 为复杂图表添加图例
- 保持图表专注于一个方面
- 有意义地使用颜色编码
- 包含标题和描述
- 对图表进行版本控制
- 使用基于文本的格式（Mermaid、PlantUML）
- 清晰显示数据流方向
- 包含部署细节
- 记录图表约定
- 使图表与代码保持同步
- 使用子图进行逻辑分组
- 标注接口和协议
- 包含错误处理路径

### ❌ 不应该做的

- 在图表中堆砌过多细节
- 使用不一致的样式
- 跳过图表图例
- 仅创建二进制图像文件
- 忘记记录关系
- 在一个图表中混合抽象级别
- 使用专有格式
- 忽略边界情况
- 省略错误处理
- 使用模糊的命名

## 常见使用场景

### 场景 1：系统设计评审

**需求**：向团队展示新系统架构

**推荐图表**：

1. C4 上下文图：展示系统与外部交互
2. C4 容器图：展示主要技术组件
3. 部署图：展示基础设施布局

### 场景 2：API 文档

**需求**：记录 API 请求流程

**推荐图表**：

1. 时序图：展示请求-响应流程
2. 数据流图：展示数据转换过程
3. 状态图：展示资源状态变化

### 场景 3：嵌入式系统开发

**需求**：设计物联网设备架构

**推荐图表**：

1. 硬件架构图：展示传感器、MCU、通信模块
2. 通信协议时序图：展示 I2C/SPI/UART 交互
3. 状态机图：展示设备运行状态
4. 数据流图：展示数据采集到上传的流程

### 场景 4：故障排查

**需求**：分析和记录系统故障

**推荐图表**：

1. 时序图：重现故障场景
2. 数据流图：识别故障点
3. 状态图：展示异常状态转换

## 工具和资源

### 在线编辑器

- **Mermaid Live Editor**: https://mermaid.live/
- **PlantUML Online**: https://www.plantuml.com/plantuml/
- **draw.io**: https://www.diagrams.net/

### VS Code 扩展

- **Mermaid Preview**: 实时预览 Mermaid 图表
- **PlantUML**: PlantUML 支持
- **Draw.io Integration**: VS Code 中的 draw.io

### 文档集成

- **Markdown**: 直接嵌入 Mermaid 代码块
- **Sphinx**: 支持 PlantUML 和 Mermaid
- **GitBook**: 原生支持 Mermaid
- **GitHub/GitLab**: 自动渲染 Mermaid

## 学习资源

- [Mermaid 官方文档](https://mermaid.js.org/)
- [PlantUML 官方文档](https://plantuml.com/)
- [C4 模型](https://c4model.com/)
- [代码即图表（Diagrams as Code）](https://diagrams.mingrammer.com/)
- [UML 教程](https://www.uml-diagrams.org/)

## 版本历史

- **v1.0.0**（2025-12-16）：初始版本
  - Mermaid 示例
  - PlantUML 示例
  - C4 模型示例
  - 嵌入式系统架构示例
  - 最佳实践指南

---

**最后更新**：2025-12-16
**Skill 类型**：Type 1（知识库）
**状态**：生产就绪
