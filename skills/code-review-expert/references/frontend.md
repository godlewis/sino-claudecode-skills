# Frontend Review Expert - 前端审查专家

## 审查范围

专注于前端代码质量、用户体验、性能优化、可访问性和浏览器兼容性。涵盖React、Vue、Angular、TypeScript、JavaScript、HTML、CSS等技术栈。

## 核心审查维度

### 1. 组件设计

#### 单一职责原则
**问题**: 组件承担过多职责
**风险等级**: 中

**反模式**:
```jsx
// ❌ 一个组件做了太多事
function UserDashboard() {
  // 获取数据
  // 处理表单
  // 显示图表
  // 管理路由
  // 处理权限
  // ... 500行代码
}
```

**最佳实践**:
```jsx
// ✅ 拆分成职责单一的小组件
function UserDashboard() {
  return (
    <>
      <UserStats />
      <UserProfile />
      <RecentActivities />
    </>
  );
}
```

#### Props设计
**问题**: Props过多、命名不清晰、类型缺失
**风险等级**: 中

**反模式**:
```jsx
// ❌ Props过多且无类型
function User({ id, name, email, age, address, phone, role, status, createdAt, ...props }) {
  // 10+ props,难以理解和维护
}
```

**最佳实践**:
```tsx
// ✅ 使用TypeScript接口,合理分组
interface UserProps {
  user: UserInfo;  // 分组相关数据
  onUpdate: (user: UserInfo) => void;
  variant?: 'default' | 'compact';
}

function User({ user, onUpdate, variant = 'default' }: UserProps) {
  // 清晰的类型定义
}
```

**审查要点**:
- Props超过5个考虑分组
- 必须使用TypeScript或PropTypes
- 布尔props使用清晰的命名(`isActive`而非`active`)

### 2. 状态管理

#### 状态提升
**问题**: 状态放在错误的层级
**风险等级**: 中

**反模式**:
```jsx
// ❌ 状态应该在父组件
function Parent() {
  return <Child />;
}

function Child() {
  const [data, setData] = useState(null);
  // data应该由Parent管理,多个Child需要共享时问题更严重
}
```

**最佳实践**:
```jsx
// ✅ 状态提升到需要的最低公共祖先
function Parent() {
  const [data, setData] = useState(null);
  return <Child data={data} onUpdate={setData} />;
}
```

#### 全局状态滥用
**问题**: 应该是本地状态却使用全局状态
**风险等级**: 中

**审查要点**:
- 表单输入状态应该是组件本地状态
- 仅跨组件共享的状态使用Redux/Zustand/Pinia
- 服务端状态使用React Query/SWR

### 3. 性能优化

#### 不必要的重渲染
**问题**: 组件频繁重渲染导致性能问题
**风险等级**: 高

**反模式**:
```jsx
// ❌ 每次父组件渲染都创建新函数
function Parent() {
  return <ExpensiveChild onClick={() => console.log('click')} />;
}

// ❌ 每次渲染都创建新对象/数组
function Parent() {
  const config = { theme: 'dark' }; // 新对象引用
  return <Child config={config} />;
}
```

**最佳实践**:
```jsx
// ✅ 使用useCallback缓存函数
function Parent() {
  const handleClick = useCallback(() => {
    console.log('click');
  }, []);
  return <ExpensiveChild onClick={handleClick} />;
}

// ✅ 使用useMemo缓存对象
function Parent() {
  const config = useMemo(() => ({ theme: 'dark' }), []);
  return <Child config={config} />;
}
```

**审查要点**:
- 搜索大列表渲染(`map` over 100+ items) - 建议虚拟化
- 检查React.memo, useMemo, useCallback的使用
- Profile组件渲染时间

#### 列表渲染优化
**问题**: 大列表渲染导致卡顿
**风险等级**: 高

**反模式**:
```jsx
// ❌ 渲染10,000个DOM节点
{items.map(item => <Item key={item.id} data={item} />)}
```

**最佳实践**:
```jsx
// ✅ 使用虚拟滚动
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={items.length}
  itemSize={50}
>
  {({ index, style }) => <Item style={style} data={items[index]} />}
</FixedSizeList>
```

#### 图片优化
**问题**: 大图片、未压缩、无响应式处理
**风险等级**: 中

**最佳实践**:
```jsx
// ✅ 使用Next.js Image或类似优化
import Image from 'next/image';

<Image
  src="/photo.jpg"
  width={500}
  height={300}
  placeholder="blur"
  loading="lazy"
/>
```

### 4. 代码质量

#### Hooks规则
**问题**: Hooks使用不当
**风险等级**: 高

**反模式**:
```jsx
// ❌ 在条件语句中调用Hook
if (condition) {
  useEffect(() => {}, []);
}

// ❌ 在循环中调用Hook
items.forEach(item => {
  useState(item.id);
});
```

**最佳实践**:
```jsx
// ✅ Hooks必须在顶层调用
useEffect(() => {
  if (condition) {
    // 条件逻辑在Hook内部
  }
}, [condition]);
```

#### 依赖数组
**问题**: useEffect/useCallback/useMemo的依赖数组不正确
**风险等级**: 高

**反模式**:
```jsx
// ❌ 缺少依赖
useEffect(() => {
  fetchData(userId);
}, []); // 应该包含userId

// ❌ 过度依赖
useEffect(() => {
  setState(value + 1);
}, [value, setState, otherUnrelatedState]);
```

**最佳实践**:
```jsx
// ✅ 正确的依赖
useEffect(() => {
  fetchData(userId);
}, [userId]); // 包含所有外部依赖
```

#### 错误边界
**问题**: 缺少错误边界
**风险等级**: 中

**最佳实践**:
```jsx
// ✅ 添加错误边界
class ErrorBoundary extends React.Component {
  // ...

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}

// 使用
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### 5. 可访问性 (A11y)

#### 语义化HTML
**问题**: 使用div而非语义化标签
**风险等级**: 中

**反模式**:
```jsx
// ❌ 使用div
<div onClick={handleClick}>Button</div>
```

**最佳实践**:
```jsx
// ✅ 使用button
<button onClick={handleClick}>Button</button>
```

#### ARIA属性
**问题**: 缺少必要的ARIA属性
**风险等级**: 中

**最佳实践**:
```jsx
// ✅ 正确的ARIA
<button
  aria-label="关闭对话框"
  aria-pressed={isPressed}
  onClick={handleClose}
>
  ×
</button>
```

**审查清单**:
- [ ] 图片有alt属性
- [ ] 表单输入有关联的label
- [ ] 按钮和链接有清晰的文本或aria-label
- [ ] 颜色不是唯一的传达信息的方式
- [ ] 键盘导航可用

### 6. CSS和样式

#### CSS-in-JS性能
**问题**: 不必要的样式计算
**风险等级**: 中

**最佳实践**:
```jsx
// ✅ 避免动态样式对象
const style = { color: theme.color }; // ❌ 每次渲染新对象

// ✅ 使用静态类名或styled-components
className={`btn ${isActive ? 'active' : ''}`}
```

#### 响应式设计
**问题**: 固定宽度,不考虑移动端
**风险等级**: 中

**最佳实践**:
```css
/* ✅ 使用相对单位和媒体查询 */
.container {
  width: 100%;
  max-width: 1200px;
  padding: 0 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.5rem;
  }
}
```

### 7. TypeScript最佳实践

#### 类型定义
**问题**: 使用`any`,类型过于宽泛
**风险等级**: 中

**反模式**:
```tsx
// ❌ 使用any
function processData(data: any): any {
  return data.result;
}
```

**最佳实践**:
```tsx
// ✅ 具体的类型定义
interface Data {
  result: string;
  timestamp: number;
}

function processData(data: Data): string {
  return data.result;
}
```

#### 类型守卫
**问题**: 未正确处理可能为null/undefined的值
**风险等级**: 中

**最佳实践**:
```tsx
// ✅ 正确的可空处理
function getUser(id: number): User | null {
  // ...
}

const user = getUser(id);
if (user) {  // 类型守卫
  console.log(user.name);
}
```

### 8. 测试

#### 测试覆盖
**问题**: 缺少测试或测试覆盖率低
**风险等级**: 中

**最佳实践**:
```tsx
// ✅ 单元测试示例
describe('UserComponent', () => {
  it('should render user name', () => {
    render(<User name="John" />);
    expect(screen.getByText('John')).toBeInTheDocument();
  });

  it('should call onUpdate when button clicked', () => {
    const onUpdate = jest.fn();
    render(<User name="John" onUpdate={onUpdate} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onUpdate).toHaveBeenCalled();
  });
});
```

## 性能指标

关注以下关键指标:

| 指标 | 良好 | 需改进 |
|------|------|--------|
| First Contentful Paint (FCP) | < 1.8s | > 3s |
| Largest Contentful Paint (LCP) | < 2.5s | > 4s |
| Time to Interactive (TTI) | < 3.8s | > 7.3s |
| Cumulative Layout Shift (CLS) | < 0.1 | > 0.25 |
| First Input Delay (FID) | < 100ms | > 300ms |

## 审查输出模板

```markdown
### [严重/高/中/低] 问题类型

**位置**: `文件路径:行号`

**问题描述**:
简明描述问题

**代码示例**:
\`\`\`jsx/tsx
// ❌ 当前代码
有问题代码
\`\`\`

**改进建议**:
\`\`\`jsx/tsx
// ✅ 建议代码
改进后代码
\`\`\`

**影响**:
- 用户体验: ...
- 性能: ...
- 可维护性: ...

**参考**: 相关最佳实践链接
```

## 工具推荐

- **代码质量**: ESLint, Prettier
- **类型检查**: TypeScript, tsc --noEmit
- **可访问性**: axe-core, WAVE
- **性能**: Lighthouse, WebPageTest
- **测试**: Jest, React Testing Library, Cypress
- **Bundle分析**: Webpack Bundle Analyzer

## 参考资源

- [React Docs - Best Practices](https://react.dev/learn)
- [Vue Style Guide](https://vuejs.org/style-guide/)
- [Angular Style Guide](https://angular.io/guide/styleguide)
- [Web.dev Performance](https://web.dev/performance/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
