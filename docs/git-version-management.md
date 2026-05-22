# Git 版本保存与回退指南

## 一、版本保存的三层体系

Git 保存版本有三个层次，从轻到重：

| 层次 | 命令 | 用途 | 是否可移动 |
|------|------|------|-----------|
| Commit | `git commit` | 记录一次代码快照 | 固定（除非强制操作） |
| Tag | `git tag` | 给重要版本打标签（如 v1.0.0） | 固定（轻量/附注标签） |
| Branch | `git branch` | 并行开发线 | 随新 commit 移动 |

### 1.1 提交（Commit）—— 最基本的版本保存

```bash
# 将文件加入暂存区
git add <file>          # 添加单个文件
git add .               # 添加所有变更

# 提交到本地仓库
git commit -m "feat: 添加用户登录功能"

# 查看提交历史
git log --oneline --graph --all
```

**提交信息规范（Conventional Commits）：**
```
feat:     新功能
fix:      bug 修复
refactor: 代码重构
docs:     文档更新
test:     测试相关
chore:    构建/工具
```

### 1.2 标签（Tag）—— 标记里程碑

```bash
# 轻量标签（仅指针）
git tag v1.0.0

# 附注标签（推荐，含作者、日期、说明）
git tag -a v1.0.0 -m "正式发布 1.0.0 版本"

# 给历史 commit 补打标签
git tag -a v0.9.0 <commit-hash> -m "测试版"

# 查看所有标签
git tag -l

# 推送标签到远程
git push origin v1.0.0        # 推送单个标签
git push origin --tags        # 推送所有标签
```

### 1.3 分支（Branch）—— 版本保存的核心策略

```bash
# 创建分支
git branch feature-login

# 切换分支
git switch feature-login       # 新命令（推荐）
git checkout feature-login     # 旧命令

# 创建并切换
git switch -c feature-login

# 查看所有分支
git branch -a
```

---

## 二、推荐的版本保存策略

### 2.1 分支策略（基于 Git Flow 简化版）

```
main        ← 生产环境，只接受 merge，不打直接 commit
  └─ develop   ← 开发主线
       ├─ feature/xxx  ← 功能分支
       ├─ fix/xxx      ← 修复分支
       └─ release/x.x  ← 发布分支
```

### 2.2 日常开发流程

```bash
# 1. 每天开始：基于最新 develop 创建功能分支
git switch develop
git pull origin develop
git switch -c feature/xxx

# 2. 频繁小提交（每完成一个逻辑单元就提交）
git add .
git commit -m "feat: 完成表单校验"

# 3. 推送功能分支到远程（备份 + 协作）
git push -u origin feature/xxx

# 4. 完成后合并回 develop
git switch develop
git pull origin develop
git merge feature/xxx
git push origin develop

# 5. 删除已合并的功能分支
git branch -d feature/xxx
git push origin --delete feature/xxx
```

### 2.3 发布版本时打 Tag

```bash
# 发布前：在 main 上打附注标签
git switch main
git pull origin main
git merge develop
git tag -a v1.2.0 -m "发布 v1.2.0：新增搜索功能，修复登录bug"
git push origin main
git push origin v1.2.0
```

---

## 三、版本回退 —— 完整工具箱

### 3.1 回退场景速查表

| 场景 | 推荐命令 | 安全性 |
|------|---------|--------|
| 撤回工作区未暂存的修改 | `git restore <file>` | 安全 |
| 撤回暂存区的文件 | `git restore --staged <file>` | 安全 |
| 撤回最近一次 commit，保留修改 | `git reset --soft HEAD~1` | 安全 |
| 撤回最近一次 commit，丢弃修改 | `git reset --hard HEAD~1` | **危险** |
| 撤回已推送的 commit（协作安全） | `git revert <commit>` | **推荐** |
| 回退到某个历史版本查看 | `git checkout <commit>` | 安全（只读） |
| 回退文件到某个历史版本 | `git restore --source=<commit> <file>` | 安全 |
| 整个仓库回退到指定版本 | `git reset --hard <commit>` | **危险** |

### 3.2 各命令详解

#### `git restore` —— 撤回未提交的修改（首选）

```bash
# 丢弃工作区某个文件的所有修改
git restore app/main.py

# 丢弃工作区所有修改
git restore .

# 将已 git add 的文件从暂存区撤回（保留文件修改）
git restore --staged app/main.py

# 将文件恢复到某个历史版本
git restore --source=<commit-hash> app/main.py
```

#### `git reset` —— 移动 HEAD 指针

```bash
# --soft：撤回 commit，修改保留在暂存区（可重新提交）
git reset --soft HEAD~1     # 撤回最近 1 次 commit
git reset --soft HEAD~3     # 撤回最近 3 次 commit

# --mixed（默认）：撤回 commit + 暂存，修改保留在工作区
git reset HEAD~1
git reset --mixed HEAD~1

# --hard：撤回一切，完全回到指定版本状态
git reset --hard HEAD~1     # ⚠️ 工作区修改全部丢失
git reset --hard <commit>   # ⚠️ 跳到指定 commit
```

**`~` 和 `^` 语法：**
```bash
HEAD~1      # HEAD 往前数 1 个 commit（等价 HEAD~）
HEAD~3      # HEAD 往前数 3 个 commit
HEAD^       # HEAD 的父 commit（等价 HEAD~1）
HEAD^^      # HEAD 的父的父（等价 HEAD~2）
```

#### `git revert` —— 协作安全回退（已推送代码首选）

```bash
# 撤销某次 commit，产生一个新的"反向" commit
git revert <commit-hash>

# 撤销最近一次 commit
git revert HEAD

# 撤销一系列 commit（范围：不包含 a，包含 b）
git revert <commit-a>..<commit-b>

# 撤销但不自动提交（便于一次撤销多个）
git revert --no-commit <commit1>
git revert --no-commit <commit2>
git commit -m "revert: 同时撤销 commit1 和 commit2"
```

> **reset vs revert 关键区别：**
> - `reset`：改写历史，旧 commit 消失。**绝不能用于已推送的公共分支。**
> - `revert`：追加新 commit，历史完整。**协作安全，永远用这个处理已推送代码。**

#### `git reflog` —— 救命稻草

```bash
# 查看 HEAD 所有历史移动记录（包括被 reset 掉的 commit）
git reflog

# 输出示例：
# a1b2c3d HEAD@{0}: commit: feat: 搜索功能
# e4f5g6h HEAD@{1}: reset: moving to HEAD~1    ← 被 reset 掉的 commit 还在这里
# i7j8k9l HEAD@{2}: commit: feat: 旧的登录

# 恢复到被 reset 前的状态
git reset --hard HEAD@{1}
# 或者用 commit hash
git reset --hard e4f5g6h
```

---

## 四、实战场景演练

### 场景 1：我刚改坏了文件，想回到修改前

```bash
# 丢弃单个文件的修改
git restore app/main.py

# 或者丢弃所有修改
git restore .
```

### 场景 2：我刚 commit 了，但 commit 信息写错了

```bash
# 修改最近一次 commit 信息
git commit --amend -m "fix: 正确的提交信息"

# 如果已经 push 了，需要强制推送（⚠️ 仅限个人分支）
git push --force-with-lease
```

### 场景 3：我刚 commit 了，但漏了文件

```bash
# 添加漏掉的文件
git add forgotten_file.py

# 追加到最近一次 commit（不会产生新 commit）
git commit --amend --no-edit

# 如果已经 push 了
git push --force-with-lease
```

### 场景 4：我 commit 了 3 次，想合并成 1 次

```bash
# 交互式变基，合并最近 3 次 commit
git rebase -i HEAD~3

# 编辑器会打开，把第 2、3 行的 pick 改成 squash（或 s）：
# pick a1b2c3d commit 1
# squash e4f5g6h commit 2
# squash i7j8k9l commit 3
# 保存退出，编辑合并后的 commit 信息
```

### 场景 5：我 commit 后发现代码有 bug，想撤回这个 commit

```bash
# 如果还没 push
git reset --soft HEAD~1    # commit 撤回，修改保留
# 改完 bug 后重新 commit

# 如果已经 push 了（协作安全方式）
git revert HEAD
git push origin main
```

### 场景 6：我已经 push 了，但发现不应该推

```bash
# 安全方式：revert
git revert HEAD
git push origin main

# 如果确定只有你一个人用这个分支（危险方式）
git reset --hard HEAD~1
git push --force-with-lease    # 用 --force-with-lease 而非 --force
```

> `--force-with-lease` 比 `--force` 安全：如果远程有别人的新 commit，它会拒绝推送。

### 场景 7：我想回到 3 天前的版本看看代码，看完再回来

```bash
# 查看 3 天前的 commit
git log --since="3 days ago" --until="2 days ago"

# 临时切换到那个版本（detached HEAD 状态）
git checkout <commit-hash>

# 看完后回到原来的分支
git switch -
```

### 场景 8：我想把某个文件恢复到一周前的版本

```bash
# 先找到那个文件在历史中的样子
git log --oneline -- app/main.py

# 恢复到指定 commit 时的版本
git restore --source=<commit-hash> app/main.py

# 提交这个恢复
git add app/main.py
git commit -m "fix: 恢复 main.py 到一周前版本"
```

### 场景 9：reset --hard 后后悔了

```bash
# 用 reflog 找回
git reflog
# 找到 reset 之前的 commit hash

git reset --hard <那个-hash>
# 或 git reset --hard HEAD@{n}
```

### 场景 10：紧急回滚线上版本

```bash
# 1. 基于当前 main 创建回滚分支（安全网）
git switch main
git switch -c rollback-v1.2.0

# 2. 找到上一个稳定版本的 tag
git tag -l

# 3. 用 revert 回退到稳定版本（安全，保留历史）
git revert --no-commit v1.2.0..HEAD
git commit -m "revert: 紧急回滚 v1.2.0，恢复到 v1.1.0 状态"

# 4. 推送并部署
git push origin rollback-v1.2.0

# 5. 打标签标记回滚点
git tag -a hotfix-rollback-20240521 -m "紧急回滚 v1.2.0"
```

---

## 五、黄金法则

### 5.1 绝对不要做的事

| 禁止操作 | 原因 |
|----------|------|
| `git reset --hard` 到已推送的公共分支 | 破坏协作者的历史 |
| `git push --force` 到 main/master | 覆盖别人的代码 |
| 在公共分支上 `git commit --amend` | 改变已共享的历史 |
| `git reset --hard` 前不检查 `git status` | 丢失未保存的修改 |

### 5.2 必须养成的习惯

1. **提交前先 `git status` 和 `git diff`** —— 确认改了什么
2. **频繁小提交** —— 每个 commit 只做一件事，方便回退
3. **关键节点打 tag** —— 发布前、大重构前、迁移前
4. **操作前先切备份分支** —— `git branch backup-xxx` 只需一行就能保命
5. **push 前先 pull** —— `git pull --rebase` 保持历史线性
6. **用 `--force-with-lease` 替代 `--force`** —— 避免覆盖别人的推送

### 5.3 安全回退决策树

```
要回退吗？
├─ 修改还没 commit？
│   └─ git restore（工作区）/ git restore --staged（暂存区）
│
├─ 已经 commit 但没 push？
│   ├─ 想保留修改 → git reset --soft HEAD~N
│   └─ 想丢弃修改 → git reset --hard HEAD~N
│
├─ 已经 push 到公共分支？
│   └─ 必须用 git revert（追加新 commit，不动历史）
│
└─ 已经 push 到个人分支且确定无协作者？
    └─ 可以用 git reset + git push --force-with-lease
```

---

## 六、速查命令汇总

```bash
# === 查看状态 ===
git status                     # 工作区状态
git log --oneline --graph -20  # 提交历史图
git reflog                     # HEAD 移动记录（救命用）
git diff                       # 工作区 vs 暂存区
git diff --staged              # 暂存区 vs 最新 commit

# === 保存版本 ===
git add <file>                 # 暂存
git commit -m "message"        # 提交
git tag -a v1.0.0 -m "msg"     # 打标签
git branch backup-xxx          # 创建备份分支

# === 回退 ===
git restore <file>             # 丢弃工作区修改
git restore --staged <file>    # 取消暂存
git restore --source=<hash> <file>  # 文件回到历史版本
git reset --soft HEAD~1        # 撤回 commit，保留修改
git reset --hard HEAD~1        # 撤回 commit + 丢弃修改
git revert <commit>            # 安全撤销（生成反向 commit）

# === 修正 ===
git commit --amend -m "msg"    # 修改最近 commit 信息
git rebase -i HEAD~3           # 交互式合并 commit
git push --force-with-lease    # 强制推送（比 --force 安全）

# === 紧急救援 ===
git reflog                     # 查看所有 HEAD 操作历史
git checkout <lost-hash>       # 找回丢失的 commit
git branch recovery <hash>     # 用丢失的 hash 创建新分支
```
