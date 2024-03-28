

## SafeTest: 下一代UI测试库


SafeTest是一个革命性的库，为基于web的用户界面(UI)应用程序提供了端到端(E2E)测试的新视角。


### 传统UI测试的问题

从根本上讲，UI测试有两种风格：集成测试和E2E测试。

集成测试通常通过`react-testing-library`或类似程序运行。它们快速、易于编写，并且可以测试应用程序中的组件。他们存在着一些缺陷。然而，它们的局限性在于并没有实际运行应用程序或将实际项目呈现到屏幕上，因此这些测试不会捕捉到诸如`index-z`错误导致提交按钮无法点击之类的回归。另一个常见的问题是，虽然编写测试的`setup`很容易，但编写导致页面上的事情发生所需的事件却很困难。例如，显示一个花哨的`＜Dropdown/＞`并不像调用`fireEvent.click（'select'）` 那么简单，因为`js-dom`与真正的浏览器并不完全匹配，所以你最终需要将鼠标悬停在标签上，然后单击`select`。同样，弄清楚如何在智能`＜Input/＞`上输入文本也有类似的挑战。弄清楚实现这一目标的确切`咒语`既困难又脆弱。调试某些东西停止工作的原因也很困难，因为你不能打开浏览器就知道发生了什么。


像`Cypress`和`Playwright`这样的E2E测试非常适合测试实际应用程序。它们使用真实的浏览器，并针对实际应用程序运行。他们能够测试`index-z`问题等。然而，他们缺乏独立测试组件的能力，这就是为什么一些团队最终会有一个与Storybook 相邻的构建来进行E2E测试。另一个问题是，很难设置不同的测试fixtrue。例如，如果你想测试管理员用户在页面上有编辑按钮，而普通用户没有，你会找到一些方法来覆盖身份验证服务，以返回不同的结果。类似地，当我们有外部服务依赖项（如OAuth）时，组件测试是不可能的，因为Cypress和Playwright组件测试不会针对应用程序的实际实例运行，因此任何身份验证都可能使渲染组件变得不可能。


通过分解，我们可以得到下面的表格：

| 集成测试[赞成者]   | 集成测试[反对者]  |  E2E测试[赞成者]   | E2E测试[反对者]  |
| ------ | ------ |------ |------ |
| Easy setup | Hard to drive | Easy to drive	| Hard to setup |
| Fast	| Hard to debug	| Easy to debug	| Slow |
| Mock services | Hard to override network | Easy to override network |	No service mocking |
|  | Can't test clickability of element |	Can test clickability of element| |
|  | Can't test z-index	| Can test z-index | |
|  | Can't easily set value on `<Input />` |	Easy to set value on `<Input />` | |
|  | No screenshot testing	| Screenshot testing | |
|  | No video recording	| Video recording | |
|  | No trace viewer	| Trace viewer | |
|  No confidence app works E2E	| Confidence components work	| Confidence app works E2E	| No confidence components work |

这两者几乎是互补的，如果有办法把两者结合起来就好了……


### SafeTest 示例

这正是Safetest试图解决的问题。Safetest 将 `集成测试`和`E2E测试`结合在一起的方式。它允许我们编写易于设置、易于驱动的测试，并且可以单独测试组件，同时还可以测试整个应用程序，测试元素的可点击性，以及进行屏幕截图测试、视频录制、跟踪查看器等。


* TS代码定义一个页面Header：

```ts
// Header.tsx
export const Header = ({ admin }: { admin?: boolean }) => (
  <div className='header'>
    <div className='header-title'>The App</div>
    <div className='header-user'>
      <div className='header-user-name'>admin</div>
      {admin && <div className='header-user-admin'>admin</div>}
      <div className='header-user-logout'>Logout</div>
    </div>
  </div>
);
```

* Safetest编写测试：

```ts
// Header.safetest.tsx
import { describe, it, expect } from 'safetest/jest';
import { render } from 'safetest/react';
import { Header } from './Header';

describe('Header', () => {
  it('can render a regular header', async () => {
    const { page } = await render(<Header />);
    await expect(page.locator('text=Logout')).toBeVisible();
    await expect(page.locator('text=admin')).not.toBeVisible();
    expect(await page.screenshot()).toMatchImageSnapshot();
  });

  it('can render an admin header', async () => {
    const { page } = await render(<Header admin={true} />);
    await expect(page.locator('text=Logout')).toBeVisible();
    await expect(page.locator('text=admin')).toBeVisible();
    expect(await page.screenshot()).toMatchImageSnapshot();
  });
});
```

如果你使用过cypress，playwright(js)等自动化工具，SafeTest对你来说非常简单。

## Safetest 特点于原理

Safetest是一个强大的UI测试库，它结合了Playwright、Jest/Vitest和React，为应用程序和组件测试提供了强大的端到端测试解决方案。

Safetest通过与现有的开发环境集成，并提供熟悉、易于使用的API来创建和管理测试，从而提供无缝的测试体验。


__特征__


* `Playwright集成`：使用Playwright在真实浏览器上运行测试。Safetest自动处理浏览器管理，因此您可以专注于编写测试。

* `Jest集成`：Safetest利用了Jest测试运行程序。使用熟悉的Jest语法编写测试，并受益于其强大的断言库和模拟功能。

* `Vitest集成`：Safetest也可以使用Vitest runner。如果你有一个vite项目，你可能会想使用这个

* `React支持`：Safetest的设计考虑到了React应用程序，因此您可以轻松地测试组件及其交互。这允许对单个组件进行集中测试，例如测试＜Header-admin＝｛true｝＞的行为是否符合预期。

* `与框架无关`：Safetest还可以与Vue、Svelte和Angular等其他框架配合使用。Safetest甚至可以对NextJS应用程序进行组件测试

* `简单的Setup`：安全测试易于设置和配置，因此您可以很快开始编写测试。无需担心复杂的配置或依赖关系；安全测试可以解决所有问题。

* `简单的Auth Hooks`：如果你的应用程序正在测试一个经过身份验证的应用程序，Safetest会提供挂钩，在所有测试中以可重复使用的方法处理身份验证流。


__原理__

SafeTest主要思想是在我们的应用程序启动节点插入一段代码，注入钩子来运行我们的测试。注意，这种工作方式对应用程序的正常使用没有影响，因为SafeTest仅在运行测试时才利用延迟加载来动态加载测试，当程序打包发布的时候不包含测试代码。然后，就可以使用`Playwright`运行常规测试，从而实现我们理想的方式控制浏览器。

