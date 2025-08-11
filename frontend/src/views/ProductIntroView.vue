    <template>
  <div class="page-container">
    <section class="hero-section-reimagined" aria-labelledby="hero-title">
      <div class="content-wrapper hero-split-layout">
        <div class="hero-left">
          <h1 id="hero-title" class="hero-main-title">
            简单、快速、可靠的
            <br />
            <span class="service-name">自助打印服务</span>
          </h1>
          <p class="hero-main-subtitle">
            从上传文件到获取取件码，体验前所未有的流畅与便捷。我们致力于让高质量打印触手可及。
          </p>
          <router-link to="/order" aria-label="前往订单页面开始打印">
            <BaseButton class="hero-cta-button">立即开始打印</BaseButton>
          </router-link>
        </div>

        <div class="hero-right" aria-hidden="true">
          <div class="hero-animation-container">
            <div class="paper-sheet sheet-3"></div>
            <div class="paper-sheet sheet-2"></div>
            <div class="paper-sheet sheet-1">
              <div
                v-for="(feature, index) in features"
                :key="feature.title"
                :class="['keyword-tag', `tag-${index + 1}`]"
                :style="{ animationDelay: `${0.5 + index * 0.2}s` }"
                role="presentation"
              >
                ✔ {{ feature.title }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="features-section" aria-labelledby="features-title">
      <div class="content-wrapper">
        <h2 id="features-title" class="section-title">核心功能</h2>
        <div class="features-grid" role="list">
          <article class="feature-card" role="listitem">
            <div class="icon-wrapper" aria-hidden="true">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="icon"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 class="feature-title">极简流程</h3>
            <p class="feature-description">通过我们精心设计的步骤引导，只需几分钟即可完成您的打印配置和下单。</p>
          </article>

          <article class="feature-card" role="listitem">
            <div class="icon-wrapper" aria-hidden="true">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="icon"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="feature-title">状态实时</h3>
            <p class="feature-description">提交订单后，您可以随时通过订单号查询打印状态和订单信息，全程透明。</p>
          </article>

          <article class="feature-card" role="listitem">
            <div class="icon-wrapper" aria-hidden="true">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="icon"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3l7 4v5c0 5.25-3.5 9.75-7 11-3.5-1.25-7-5.75-7-11V7l7-4z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v6m-3-3h6" />
              </svg>
            </div>
            <h3 class="feature-title">品质保证</h3>
            <p class="feature-description">我们采用高质量的打印设备和材料，确保每一份文件都呈现出最佳的效果。</p>
          </article>
        </div>
      </div>
    </section>

    <section class="stats-section" ref="statsSection" aria-labelledby="stats-title">
      <div class="content-wrapper">
        <h2 id="stats-title" class="visually-hidden">服务统计数据</h2>
        <div class="stats-grid" role="list">
          <div class="stat-item" role="listitem">
            <span class="stat-number" :aria-label="`累计打印${pageCountDisplay.toLocaleString()}页`">
              {{ pageCountDisplay.toLocaleString() }}
            </span>
            <p class="stat-label">累计打印页数</p>
          </div>
          <div class="stat-item" role="listitem">
            <span class="stat-number" :aria-label="`服务${userCountDisplay.toLocaleString()}位用户`">
              {{ userCountDisplay.toLocaleString() }}
            </span>
            <p class="stat-label">服务用户数</p>
          </div>
          <div class="stat-item" role="listitem">
            <span class="stat-number" :aria-label="`用户好评率${satisfactionRateDisplay}%`">
              {{ satisfactionRateDisplay }}%
            </span>
            <p class="stat-label">用户好评率</p>
          </div>
        </div>
      </div>
    </section>



    <!-- 全新设计的流程演示部分 -->
    <section class="workflow-showcase" ref="workflowSection" aria-labelledby="workflow-title">
      <div class="workflow-container">
        <div class="content-wrapper">
          <div class="workflow-header">
            <h2 id="workflow-title" class="section-title">
              3步极简流程
              <span class="subtitle">从上传到取件，就是这么简单</span>
            </h2>
          </div>

          <!-- 流程导航 -->
          <div class="workflow-navigation">
                        <div
              v-for="(step, index) in workflowSteps"
              :key="step.id"
              :class="['nav-step', { active: currentWorkflowStep === index + 1 }]"
              @click="setWorkflowStep(index + 1)"
              @keydown.enter="setWorkflowStep(index + 1)"
              @keydown.space.prevent="setWorkflowStep(index + 1)"
              :aria-label="`切换到步骤${index + 1}: ${step.title}`"
              role="button"
              tabindex="0"
            >
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-label">{{ step.title }}</div>
            </div>

            <!-- 连接线 -->
            <div class="connection-line">
              <div class="progress-line" :style="{ width: progressWidth }"></div>
            </div>
          </div>

          <!-- 主要演示区域 -->
          <div class="workflow-demo">
            <!-- 左侧：分步说明 -->
            <div class="step-explanation">
              <transition name="slide-fade" mode="out-in">
                <div v-if="currentWorkflowStep === 1" class="explanation-content" key="step1">
                  <div class="step-icon upload-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                    </svg>
                  </div>
                  <h3>上传文件</h3>
                  <p>拖拽或点击上传您的文档，支持PDF、Word、PPT等多种格式。文件会被安全加密传输。</p>
                  <div class="feature-highlights">
                    <div class="highlight-item">
                      <span class="icon">🔒</span>
                      <span>加密传输</span>
                    </div>
                    <div class="highlight-item">
                      <span class="icon">⚡</span>
                      <span>极速上传</span>
                    </div>
                    <div class="highlight-item">
                      <span class="icon">📁</span>
                      <span>多格式支持</span>
                    </div>
                  </div>
                </div>

                <div v-else-if="currentWorkflowStep === 2" class="explanation-content" key="step2">
                  <div class="step-icon settings-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <circle cx="12" cy="12" r="3"/>
                      <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
                    </svg>
                  </div>
                  <h3>个性化设置</h3>
                  <p>选择纸张规格、打印方式、装订选项等。实时预览费用，所见即所得。</p>
                  <div class="feature-highlights">
                    <div class="highlight-item">
                      <span class="icon">📏</span>
                      <span>多种规格</span>
                    </div>
                    <div class="highlight-item">
                      <span class="icon">💰</span>
                      <span>实时计价</span>
                    </div>
                    <div class="highlight-item">
                      <span class="icon">🎯</span>
                      <span>精确配置</span>
                    </div>
                  </div>
                </div>

                <div v-else-if="currentWorkflowStep === 3" class="explanation-content" key="step3">
                  <div class="step-icon complete-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </div>
                  <h3>完成取件</h3>
                  <p>支付成功后获取取件码，按时到服务点取件。全程状态实时更新，让您安心等待。</p>
                  <div class="feature-highlights">
                    <div class="highlight-item">
                      <span class="icon">📱</span>
                      <span>邮件通知</span>
                    </div>
                    <div class="highlight-item">
                      <span class="icon">⏰</span>
                      <span>准时完成</span>
                    </div>
                    <div class="highlight-item">
                      <span class="icon">✅</span>
                      <span>质量保证</span>
                    </div>
                  </div>
                </div>
              </transition>
            </div>

            <!-- 右侧：互动演示 -->
            <div class="interactive-demo">
              <div class="demo-device">
                <div class="device-frame">
                  <!-- 设备屏幕 -->
                  <div class="device-screen">
                    <transition name="screen-slide" mode="out-in">
                      <!-- 步骤1：文件上传演示 -->
                      <div v-if="currentWorkflowStep === 1" class="demo-screen upload-demo" key="demo1">
                        <div class="demo-header">
                          <div class="demo-title">上传文件</div>
                          <div class="demo-progress">1/3</div>
                        </div>

                        <div class="upload-zone" :class="{ 'drag-active': isDragActive }" @click="simulateUpload">
                          <div class="upload-icon-large">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                            </svg>
                          </div>
                          <p>拖拽文件到这里</p>
                          <span class="supported-formats">支持 PDF、DOC、PPT 等格式</span>
                        </div>

                        <!-- 模拟上传的文件列表 -->
                        <div v-if="showUploadedFiles" class="uploaded-files">
                          <div v-for="file in demoFiles" :key="file.id" class="file-item">
                            <div class="file-icon">📄</div>
                            <div class="file-info">
                              <div class="file-name">{{ file.name }}</div>
                              <div class="file-size">{{ file.size }}</div>
                            </div>
                            <div class="file-status">✅</div>
                          </div>
                        </div>
                      </div>

                      <!-- 步骤2：设置演示 -->
                      <div v-else-if="currentWorkflowStep === 2" class="demo-screen settings-demo" key="demo2">
                        <div class="demo-header">
                          <div class="demo-title">打印设置</div>
                          <div class="demo-progress">2/3</div>
                        </div>

                        <div class="settings-grid">
                          <div class="setting-group">
                            <label>纸张规格</label>
                            <select v-model="demoSettings.paperSize">
                              <option value="a4">A4 (210×297mm)</option>
                              <option value="a3">A3 (297×420mm)</option>
                            </select>
                          </div>

                          <div class="setting-group">
                            <label>打印方式</label>
                            <div class="radio-group">
                              <label><input type="radio" v-model="demoSettings.printMode" value="single"> 单面</label>
                              <label><input type="radio" v-model="demoSettings.printMode" value="double"> 双面</label>
                            </div>
                          </div>

                          <div class="setting-group">
                            <label>装订方式</label>
                            <select v-model="demoSettings.binding">
                              <option value="none">无装订</option>
                              <option value="staple">订书钉</option>
                              <option value="spiral">螺旋装订</option>
                            </select>
                          </div>
                        </div>

                        <div class="price-preview">
                          <div class="price-row">
                            <span>页数：{{ demoSettings.pages }}页</span>
                            <span>¥{{ (demoSettings.pages * 0.15).toFixed(2) }}</span>
                          </div>
                          <div class="price-row total">
                            <span>总计</span>
                            <span>¥{{ calculateDemoPrice }}</span>
                          </div>
                        </div>
                      </div>

                      <!-- 步骤3：完成演示 -->
                      <div v-else-if="currentWorkflowStep === 3" class="demo-screen complete-demo" key="demo3">
                        <div class="demo-header">
                          <div class="demo-title">订单完成</div>
                          <div class="demo-progress">3/3</div>
                        </div>

                        <div class="success-animation">
                          <div class="checkmark-circle">
                            <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                              <circle class="checkmark-circle-path" cx="26" cy="26" r="25" fill="none"/>
                              <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                            </svg>
                          </div>
                        </div>

                        <div class="order-summary">
                          <h4>订单提交成功！</h4>
                          <div class="pickup-code-demo">
                            <span class="code-label">您的取件码</span>
                            <div class="pickup-code-large">P-{{ String(Date.now()).slice(-3) }}</div>
                          </div>

                          <div class="order-details">
                            <div class="detail-row">
                              <span>预计完成时间</span>
                              <span>{{ estimatedTime }}</span>
                            </div>
                            <div class="detail-row">
                              <span>服务地点</span>
                              <span>校内服务点</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </transition>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 底部CTA -->
          <div class="workflow-cta">
            <p class="cta-description">准备好体验这个简单的流程了吗？</p>
            <div class="cta-buttons">
              <BaseButton class="primary-cta" @click="() => { console.log('Navigating to order page'); router.push('/order'); }">
                立即开始打印
              </BaseButton>
              <button class="secondary-cta" @click="playDemo">
                <span class="play-icon">▶</span>
                观看演示动画
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="testimonials-section" aria-labelledby="testimonials-title">
      <div class="content-wrapper">
        <h2 id="testimonials-title" class="section-title">听听我们的用户怎么说</h2>
        <div class="testimonials-grid" role="list">
           <blockquote class="testimonial-card" role="listitem">
            <p class="testimonial-quote">"这彻底改变了我们的打印流程。以往需要花费大量精力处理订单，并与用户沟通和确认打印稿件，现在在后台点击就能搞定，效率非常棒！"</p>
            <footer class="testimonial-author">
              <cite class="author-name">Xicheng2003, 开发者</cite>
            </footer>
          </blockquote>

          <blockquote class="testimonial-card" role="listitem">
            <p class="testimonial-quote">"作为一名学生，我经常需要打印大量的论文和资料。这里的价格公道，而且订单追踪功能让我非常安心，总能准时拿到我的文件。"</p>
            <footer class="testimonial-author">
              <cite class="author-name">王同学, 大学生</cite>
            </footer>
          </blockquote>

          <blockquote class="testimonial-card" role="listitem">
            <p class="testimonial-quote">"传统用微信（即时通讯工具）去沟通调整打印参数，费时费力，沟通繁琐，现在自助下单一键解决。这里的服务非常可靠，从未出过差错，是我们可以信赖的合作伙伴。"</p>
            <footer class="testimonial-author">
              <cite class="author-name">张同学, 大学生</cite>
            </footer>
          </blockquote>
        </div>
      </div>
    </section>

    <section class="cta-section" aria-labelledby="cta-title">
      <div class="content-wrapper cta-content">
        <!-- 品牌Logo -->
        <div class="cta-logo">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M7 17H5C3.89543 17 3 16.1046 3 15V11C3 9.89543 3.89543 9 5 9H19C20.1046 9 21 9.89543 21 11V15C21 16.1046 20.1046 17 19 17H17" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 9V7C17 5.89543 16.1046 5 15 5H9C7.89543 5 7 5.89543 7 7V9" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="7" y="13" width="10" height="8" rx="1" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 13H19V11" stroke="var(--color-heading)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h2 id="cta-title" class="cta-title">准备好体验便捷的打印服务了吗？</h2>
        <p class="cta-description">Printerify，为每一次打印赋能。</p>
        <p class="cta-description">立即开始，享受高质量的打印体验！</p>
        <router-link to="/order" aria-label="前往订单页面开始使用打印服务">
           <BaseButton class="cta-button">立即开始打印</BaseButton>
        </router-link>
      </div>
    </section>

    <section class="faq-section" aria-labelledby="faq-title">
      <div class="content-wrapper">
        <h2 id="faq-title" class="section-title">常见问题解答</h2>
        <div class="faq-container" role="list">
          <details class="faq-item" role="listitem">
            <summary class="faq-question" aria-expanded="false">Printerify 支持哪些文件格式？</summary>
            <div class="faq-answer" id="faq-1-answer" role="region">
              <p>Printerify 支持主流的文档格式，包括 PDF, DOC, DOCX, PPT, PPTX, JPG, PNG 等。为了获得最佳打印效果，我们强烈推荐您上传 PDF 文件。</p>
            </div>
          </details>
          <details class="faq-item" role="listitem">
            <summary class="faq-question" aria-expanded="false">使用 Printerify 如何收取费用？</summary>
            <div class="faq-answer" id="faq-2-answer" role="region">
              <p>Printerify 的收费标准主要根据订单的页数、纸张类型和其他附加服务来计算。具体计费规则说明可在自助打印下单页面点击查看。在下单过程中，您也可以在确认订单前查看详细的费用明细。</p>
            </div>
          </details>

          <details class="faq-item" role="listitem">
            <summary class="faq-question" aria-expanded="false">在 Printerify 打印需要多长时间？</summary>
            <div class="faq-answer" id="faq-3-answer" role="region">
              <p>生产时间取决于您的订单复杂程度和当前排队情况，通常在8小时内完成。具体订单状态可在订单查询页面查看。</p>
            </div>
          </details>

          <details class="faq-item" role="listitem">
            <summary class="faq-question" aria-expanded="false">Printerify 有哪些打印规格可供选择？</summary>
            <div class="faq-answer" id="faq-4-answer" role="region">
              <p>Printerify 提供多种打印规格选项，包括纸张大小（如 A4、B5）、单/双面（单面打印或双面打印）等，请以实际下单页面提供的选项为准。您可以在下单时根据需要选择合适的打印规格。</p>
            </div>
          </details>

          <details class="faq-item" role="listitem">
            <summary class="faq-question" aria-expanded="false">如果我对打印质量不满意怎么办？</summary>
            <div class="faq-answer" id="faq-5-answer" role="region">
              <p>Printerify 对打印质量有严格的把控。如果您收到的成品有任何质量问题（如错印、装订错误等），请立即联系我们的客服，我们将为您免费重印或进行退款处理。</p>
            </div>
          </details>

          <details class="faq-item" role="listitem">
            <summary class="faq-question" aria-expanded="false">如何获取 Printerify 的服务支持？</summary>
            <div class="faq-answer" id="faq-6-answer" role="region">
              <p>如果您在使用 Printerify 的过程中遇到任何问题或需要帮助，请随时联系我们的客服团队。</p>
              <p>您可以通过以下方式获取支持：</p>
              <ul>
                <li>访问我们的产品页面，查阅常见问题解答和使用指南。</li>
                <li>通过在线聊天工具（微信群或QQ群）与我们的客服代表实时沟通。</li>
                <li>用户群的加入方式可以发送邮件至 xicheng.lin@foxmail.com，我们会尽快邀请您加入。</li>
                <li>其他事宜也可发送电子邮件至 xicheng.lin@foxmail.com，我们会尽快回复您。</li>
              </ul>
            </div>
          </details>
        </div>
      </div>
    </section>



  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import BaseButton from '@/components/BaseButton.vue';

// 路由器实例
const router = useRouter();

// ==================== 常量定义 ====================
// 动画相关常量
const ANIMATION_DURATIONS = {
  counter: 2500,
  satisfaction: 3000
};

// 统计数据目标值
const STATS_TARGETS = {
  pageCount: 1089,
  userCount: 46,
  satisfactionRate: 99
};

// Intersection Observer 配置
const OBSERVER_CONFIG = {
  threshold: 0.5
};

// ==================== 数据定义 ====================

// Hero 区块功能特性
const features = ref([
  { title: '简单' },
  { title: '快速' },
  { title: '可靠' },
]);

// ==================== 流程演示相关状态 ====================
const workflowSection = ref(null);
const currentWorkflowStep = ref(1);

// 工作流程步骤定义
const workflowSteps = ref([
  { id: 'upload', title: '上传文件' },
  { id: 'settings', title: '个性设置' },
  { id: 'complete', title: '完成取件' }
]);

// 演示相关状态
const isDragActive = ref(false);
const showUploadedFiles = ref(false);
const demoFiles = ref([
  { id: 1, name: '毕业论文.pdf', size: '2.3 MB' },
  { id: 2, name: '答辩PPT.pptx', size: '1.8 MB' }
]);

// 演示设置状态
const demoSettings = ref({
  paperSize: 'a4',
  printMode: 'double',
  binding: 'staple',
  pages: 25
});

// 原滚动相关逻辑已移除，新版本使用手动交互控制

// ==================== 示例数据 ====================
// 创建符合 BindingGroup 和 DocumentItem 期望的模拟数据（保留备用）
// const sampleGroup = ref({
//   id: 'sample-group-1',
//   index: '1',
//   bindingType: 'staple_top_left',
//   documents: [
//     {
//       id: 'sample-doc-1',
//       fileName: '项目开题报告.pdf',
//       isUploading: false,
//       isRecalculating: false,
//       uploadProgress: 100,
//       pageCount: 25,
//       printCost: '3.75',
//       error: null,
//       settings: {
//         copies: 1,
//         colorMode: 'black_white',
//         printSided: 'double',
//         paperSize: 'a4',
//       }
//     },
//     {
//       id: 'sample-doc-2',
//       fileName: '答辩演示文稿_v3.pptx',
//       pageCount: 42,
//       printCost: '21.00',
//       isUploading: false,
//       isRecalculating: false,
//       uploadProgress: 100,
//       error: null,
//       settings: {
//         copies: 1,
//         colorMode: 'black_white',
//         printSided: 'single',
//         paperSize: 'a4',
//       }
//     }
//   ]
// });

// 计算示例订单总成本（保留以防Future使用）
// const sampleTotalCost = computed(() => {
//   return sampleGroup.value.documents
//     .reduce((total, doc) => total + parseFloat(doc.printCost), 0)
//     .toFixed(2);
// });

// ==================== 新流程演示相关计算属性和方法 ====================

// 进度条宽度计算
const progressWidth = computed(() => {
  return `${((currentWorkflowStep.value - 1) / (workflowSteps.value.length - 1)) * 100}%`;
});

// 演示价格计算
const calculateDemoPrice = computed(() => {
  const basePricePerPage = 0.15;
  const bindingCost = demoSettings.value.binding === 'spiral' ? 2.0 :
                     demoSettings.value.binding === 'staple' ? 0.5 : 0;
  return (demoSettings.value.pages * basePricePerPage + bindingCost).toFixed(2);
});

// 预计完成时间
const estimatedTime = computed(() => {
  const now = new Date();
  const estimated = new Date(now.getTime() + 4 * 60 * 60 * 1000); // 4小时后
  return estimated.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
});

// 设置工作流程步骤
const setWorkflowStep = (step) => {
  console.log('Setting workflow step to:', step); // 调试日志
  currentWorkflowStep.value = step;

  // 重置演示状态
  if (step === 1) {
    showUploadedFiles.value = false;
    isDragActive.value = false;
  }
};

// 模拟文件上传
const simulateUpload = () => {
  console.log('Simulating upload...'); // 调试日志
  isDragActive.value = true;

  setTimeout(() => {
    isDragActive.value = false;
    showUploadedFiles.value = true;
    console.log('Upload simulation completed'); // 调试日志
  }, 1500);
};

// 播放演示动画
const playDemo = () => {
  console.log('Starting demo playback...'); // 调试日志
  currentWorkflowStep.value = 1;
  showUploadedFiles.value = false;

  // 自动播放流程
  const autoPlay = async () => {
    try {
      console.log('Auto-play sequence started');

      // 步骤1：上传演示
      await new Promise(resolve => setTimeout(resolve, 1000));
      simulateUpload();

      await new Promise(resolve => setTimeout(resolve, 2500));

      // 步骤2：设置演示
      console.log('Moving to step 2');
      currentWorkflowStep.value = 2;
      await new Promise(resolve => setTimeout(resolve, 2000));

      // 步骤3：完成演示
      console.log('Moving to step 3');
      currentWorkflowStep.value = 3;
      await new Promise(resolve => setTimeout(resolve, 3000));

      // 重置到第一步
      console.log('Resetting to step 1');
      currentWorkflowStep.value = 1;
      showUploadedFiles.value = false;
      console.log('Demo playback completed');
    } catch (error) {
      console.error('Demo playback error:', error);
    }
  };

  autoPlay();
};

// ==================== 统计数据动画 ====================
const statsSection = ref(null);
const startAnimation = ref(false);
const pageCountDisplay = ref(0);
const userCountDisplay = ref(0);
const satisfactionRateDisplay = ref(0);

/**
 * 数值动画函数
 * @param {number} from - 起始值
 * @param {number} to - 目标值
 * @param {number} duration - 动画持续时间
 * @param {Function} onUpdate - 更新回调
 */
const animateValue = (from, to, duration, onUpdate) => {
  const startTimestamp = performance.now();

  const update = () => {
    const elapsed = performance.now() - startTimestamp;
    const progress = Math.min(1, elapsed / duration);
    // 使用缓出动画效果
    const easedProgress = 1 - Math.pow(1 - progress, 3);
    const currentValue = Math.floor(from + (to - from) * easedProgress);

    onUpdate(currentValue);

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      onUpdate(to);
    }
  };

  requestAnimationFrame(update);
};

/**
 * 启动统计数据动画
 */
const startStatsAnimation = () => {
  animateValue(0, STATS_TARGETS.pageCount, ANIMATION_DURATIONS.counter,
    (val) => pageCountDisplay.value = val);
  animateValue(0, STATS_TARGETS.userCount, ANIMATION_DURATIONS.counter,
    (val) => userCountDisplay.value = val);
  animateValue(0, STATS_TARGETS.satisfactionRate, ANIMATION_DURATIONS.satisfaction,
    (val) => satisfactionRateDisplay.value = val);
};

// 监听动画触发状态
watch(startAnimation, (isTriggered) => {
  if (isTriggered) {
    startStatsAnimation();
  }
});

/**
 * 处理统计区域滚动（Intersection Observer 回调）
 */
const handleStatsScroll = (entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !startAnimation.value) {
      startAnimation.value = true;
      observer.unobserve(statsSection.value);
    }
  });
};

// ==================== 生命周期管理 ====================
let statsObserver = null;

/**
 * 组件挂载时的初始化
 */
onMounted(() => {
  console.log('ProductIntroView mounted'); // 调试日志
  console.log('Current workflow step:', currentWorkflowStep.value);
  console.log('Workflow steps:', workflowSteps.value);
  console.log('Available functions:', {
    setWorkflowStep: typeof setWorkflowStep,
    simulateUpload: typeof simulateUpload,
    playDemo: typeof playDemo
  });

  // 创建 Intersection Observer 用于统计动画
  statsObserver = new IntersectionObserver(handleStatsScroll, OBSERVER_CONFIG);
  if (statsSection.value) {
    statsObserver.observe(statsSection.value);
  }

  // 测试功能是否工作
  setTimeout(() => {
    console.log('Testing workflow step change...');
    // 不实际改变，只是测试函数是否存在
    console.log('setWorkflowStep function is ready');
  }, 1000);
});

/**
 * 组件卸载时的清理
 */
onUnmounted(() => {
  // 断开 Intersection Observer
  if (statsObserver) {
    statsObserver.disconnect();
    statsObserver = null;
  }
});
</script>

<style scoped>

/* Scoped styles using CSS variables from main.css */
.page-container {
  color: var(--color-text);
  background-color: var(--color-background);
}

/* 无障碍辅助类 */
.visually-hidden {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}



.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-title {
  text-align: center;
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 3rem;
}

/* ==================================================== */
/* Hero Section 样式                                  */
/* ==================================================== */


/* ==================================================== */
/* 【重要样式更新】全新 Hero Section 样式         */
/* ==================================================== */

.hero-section-reimagined {
  background-color: var(--color-background-soft);
  padding: 6rem 2rem;
  min-height: 80vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-split-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4rem;
}

.hero-right {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1000px; /* 创造3D透视效果 */
  width: 100%;
}

/* 【重要样式更新】调整左侧文字排版 */
.hero-left {
  flex: 1;
  max-width: 550px;
  animation: fade-in-left 0.8s ease-out;
  width: 100%;
}

.hero-main-title {
  font-size: 2.9rem; /* 略微增大核心优势字号 */
  font-weight: 700;
  color: var(--color-heading);
  line-height: 1.5; /* 调整行高 */
  margin-bottom: 1.5rem;
}

/* 新增：为标题中的服务名设置独立样式 */
.hero-main-title .service-name {
  font-size: 2.5rem; /* 字号比主标题略小 */
  font-weight: 600; /* 字重更细 */
  color: var(--color-text); /* 颜色更柔和 */
}

.hero-main-subtitle {
  font-size: 1.0rem; /* 减小副标题字号 */
  color: var(--color-text);
  margin-bottom: 2.5rem;
  max-width: 500px;
  line-height: 1.7; /* 增加行高，提升可读性 */
}

.hero-cta-button {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
}

/* 动画容器 */
.hero-animation-container {
  position: relative;
  width: 350px;
  height: 350px;
  transform: rotateY(-25deg) rotateX(15deg);
  transform-style: preserve-3d;
  animation: float 6s ease-in-out infinite;
}

/* 【重要样式更新】纸张样式，不受暗黑模式影响 */
.paper-sheet {
  position: absolute;
  width: 80%;
  height: 100%;
  border-radius: 12px;
  /* 将边框颜色固定为浅灰色 */
  border: 1px solid #dee2e6;
  box-shadow: 0 10px 30px -5px rgba(0,0,0,0.1);
  transition: transform 0.5s ease;
}

.sheet-1 {
  /* 将顶层纸张背景固定为纯白色 */
  background: #ffffff;
  transform: translateZ(20px);
}
.sheet-2 {
  /* 将中层纸张背景固定为极浅的灰色 */
  background: #f8f9fa;
  transform: translateZ(10px) translateX(5px) translateY(5px);
}
.sheet-3 {
  /* 将底层纸张背景固定为略深的灰色，以营造堆叠感 */
  background: #e9ecef;
  transform: translateZ(0px) translateX(10px) translateY(10px);
}

/* 关键词标签样式 */
.keyword-tag {
  position: absolute;
  background-color: var(--color-primary-soft);
  color: var(--color-primary);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 1rem;
  border: 1px solid var(--color-primary);
  box-shadow: 0 2px 5px rgba(var(--color-primary-rgb), 0.1);
  opacity: 0;
  animation: fade-in-stamp 0.5s ease-out forwards;
}

.tag-1 { top: 20%; left: 15%; }
.tag-2 { top: 45%; right: 15%; }
.tag-3 { bottom: 15%; left: 15%; }

/* 响应式布局 */
@media (max-width: 982px) {
  .hero-split-layout {
    flex-direction: column-reverse;
    text-align: center;
    gap: 5rem;
  }
  .hero-right {
    margin-top: 1rem;
  }
  .hero-main-subtitle {
    margin-left: auto;
    margin-right: auto;
  }
}

@media (max-width: 767px) {
  .hero-main-title { font-size: 2rem; }
  .hero-main-subtitle { font-size: 1rem; }
  .hero-main-title .service-name { font-size: 1.85rem; }
  .hero-cta-button { padding: 0.75rem 2rem; font-size: 1rem; }

  /* 【重要更新】调整动画容器和标签在移动端的尺寸与定位 */
  .hero-animation-container {
    /* 缩小动画容器的基础尺寸，以适应移动端屏幕 */
    width: 300px;
    height: 300px;
    transform: scale(0.8) rotateY(-25deg) rotateX(15deg);
  }

  /* 为关键词标签设置一个更紧凑的字体和内边距 */
  .keyword-tag {
    font-size: 0.9rem;
    padding: 0.4rem 0.8rem;
  }

  /* 将标签的位置向内收，防止溢出 */
  .tag-1 { top: 20%; left: 10%; }
  .tag-2 { top: 45%; right: 10%; }
  .tag-3 { bottom: 15%; left: 15%; }
}

/* 【推荐补充】针对极小屏幕的优化 */
@media (max-width: 420px) {
  .hero-animation-container {
    /* 在非常窄的屏幕上进一步缩小动画容器 */
    width: 280px;
    height: 280px;
  }

  .keyword-tag {
    font-size: 0.8rem;
  }
}

/* 动画定义 */
@keyframes float {
  0% { transform: translateY(0px) rotateY(-25deg) rotateX(15deg); }
  50% { transform: translateY(-20px) rotateY(-25deg) rotateX(15deg); }
  100% { transform: translateY(0px) rotateY(-25deg) rotateX(15deg); }
}

@keyframes fade-in-left {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fade-in-stamp {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* ==================================================== */
/* Features, Stats, Testimonials, FAQ, CTA Sections     */
/* ==================================================== */

.features-section,
.testimonials-section,
.faq-section,
.cta-section {
  padding: 5rem 2rem;
}
.stats-section {
  padding: 4rem 2rem;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.features-grid, .stats-grid, .testimonials-grid {
  display: grid;
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}

.features-grid, .stats-grid {
  grid-template-columns: repeat(1, 1fr);
}

@media (min-width: 768px) {
  .features-grid, .stats-grid, .testimonials-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .testimonials-grid {
      grid-template-columns: repeat(1, 1fr);
  }
}
@media (min-width: 992px) {
    .testimonials-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}


.feature-card {
  text-align: center;
  padding: 2rem;
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.feature-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-card); }

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  background-color: var(--color-primary-soft, #ebf4ff);
  color: var(--color-primary);
  margin-bottom: 1.5rem;
}
.icon-wrapper .icon { width: 2rem; height: 2rem; }
.feature-title { font-size: 1.25rem; font-weight: 600; color: var(--color-heading); margin-bottom: 0.5rem; }
.feature-description { color: var(--color-text); line-height: 1.6; }

.stat-item { padding: 1rem; text-align: center; }
.stat-number { font-size: 3rem; font-weight: 800; color: var(--color-primary); line-height: 1; }
.stat-label { margin-top: 0.5rem; font-size: 1rem; color: var(--color-text); letter-spacing: 0.05em; text-transform: uppercase; }

/* Testimonials Section */
.testimonials-section {
  padding: 5rem 2rem;
  background-color: var(--color-background);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}

@media (min-width: 992px) {
  .testimonials-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.testimonial-card {
  background-color: var(--color-background-soft);
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

.testimonial-quote {
  font-style: italic;
  color: var(--color-text);
  margin-bottom: 1.5rem;
  flex-grow: 1;
  z-index: 1;
}

.testimonial-card::before {
  content: '“';
  font-size: 5rem;
  font-weight: bold;
  color: var(--color-border);
  position: absolute;
  left: 1rem;
  top: 0.5rem;
  z-index: 0;
  line-height: 1;
}

.testimonial-author {
  text-align: right;
  font-weight: 600;
  color: var(--color-heading);
}

/* FAQ Section Styles */
.faq-section {
  padding: 5rem 2rem;
  background-color: var(--color-background-soft);
}
.faq-section h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.7rem;
  font-weight: 700;
  color: var(--color-heading);
}
.faq-container {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  border-bottom: 1px solid var(--color-border);
}
.faq-item:first-of-type {
  border-top: 1px solid var(--color-border);
}

.faq-question {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--color-heading);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  list-style: none; /* remove default marker */
  padding: 1.5rem 0;
}

.faq-question::-webkit-details-marker {
  display: none; /* remove default marker for webkit browsers */
}

.faq-question::after {
  content: '+';
  font-size: 1.5rem;
  font-weight: 300;
  transition: transform 0.2s ease-in-out;
}

details[open] > summary.faq-question::after {
  content: '−';
}

.faq-answer {
  color: var(--color-text);
  padding: 0 0 1.5rem 0;
  line-height: 1.7;
}

/* CTA Section Styles */
.cta-section {
  background-color: var(--color-background);
  padding: 5rem 2rem;
  text-align: center;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-logo {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
  animation: logo-fade-in 0.8s ease-out;
}

.cta-logo svg {
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
  transition: transform 0.3s ease, filter 0.3s ease;
}

.cta-logo svg:hover {
  transform: scale(1.05);
  filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.15));
}

@keyframes logo-fade-in {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.cta-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 1.5rem;
}

.cta-description {
  font-size: 1rem;
  color: var(--color-text);
  margin-bottom: 1.75rem;
  line-height: 0.75;
}

.cta-button {
    font-size: 1.2rem;
    padding: 1rem 2rem;
}


/* ==================================================== */
/* 全新流程演示 Section                               */
/* ==================================================== */

.workflow-showcase {
  background: linear-gradient(135deg, var(--color-background-soft) 0%, var(--color-background) 100%);
  padding: clamp(4rem, 10vw, 8rem) 2rem;
  position: relative;
  overflow: hidden;
}

.workflow-showcase::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(0,0,0,0.05)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
  pointer-events: none;
}

.workflow-container {
  position: relative;
  z-index: 1;
}

.workflow-header {
  text-align: center;
  margin-bottom: clamp(3rem, 6vw, 5rem);
}

.workflow-header .section-title {
  position: relative;
  margin-bottom: 1rem;
}

.workflow-header .subtitle {
  display: block;
  font-size: clamp(1rem, 2vw, 1.25rem);
  font-weight: 400;
  color: var(--color-text);
  margin-top: 0.5rem;
  opacity: 0.8;
}

/* 流程导航 */
.workflow-navigation {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: clamp(3rem, 6vw, 4rem);
  position: relative;
  flex-wrap: wrap;
  gap: 1rem;
}

.nav-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 1rem;
  border-radius: 12px;
  position: relative;
  z-index: 2;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

.nav-step:hover {
  background-color: var(--color-background-soft);
  transform: translateY(-2px);
}

.nav-step.active {
  background-color: var(--color-primary-soft);
  color: var(--color-primary);
}

.nav-step:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.step-number {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background-color: var(--color-border);
  color: var(--color-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  position: relative;
}

.nav-step.active .step-number {
  background-color: var(--color-primary);
  color: white;
  transform: scale(1.1);
}

.nav-step.active .step-number::after {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border: 2px solid var(--color-primary);
  border-radius: 50%;
  opacity: 0.3;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.1;
  }
  100% {
    transform: scale(1);
    opacity: 0.3;
  }
}

.step-label {
  font-size: 0.9rem;
  font-weight: 500;
  text-align: center;
  white-space: nowrap;
  transition: color 0.3s ease;
}

.connection-line {
  position: absolute;
  top: 50%;
  left: 20%;
  right: 20%;
  height: 2px;
  background-color: var(--color-border);
  z-index: 1;
  border-radius: 1px;
}

.progress-line {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-soft));
  border-radius: 1px;
  transition: width 0.5s ease;
  position: relative;
}

.progress-line::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 8px;
  height: 8px;
  background-color: var(--color-primary);
  border-radius: 50%;
  transform: translateX(50%);
  box-shadow: 0 0 8px rgba(var(--color-primary-rgb), 0.5);
}

/* 主要演示区域 */
.workflow-demo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(3rem, 6vw, 5rem);
  align-items: center;
  margin-bottom: clamp(3rem, 6vw, 4rem);
}

/* 左侧说明 */
.step-explanation {
  padding: clamp(1.5rem, 3vw, 2rem);
}

.explanation-content {
  text-align: left;
}

.step-icon {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  position: relative;
}

.step-icon svg {
  width: 2rem;
  height: 2rem;
}

.upload-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.settings-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.complete-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.explanation-content h3 {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 1rem;
}

.explanation-content p {
  font-size: clamp(1rem, 1.8vw, 1.1rem);
  color: var(--color-text);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.feature-highlights {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--color-background-soft);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  border: 1px solid var(--color-border);
}

.highlight-item .icon {
  font-size: 1rem;
}

/* ==================== 流程演示补充样式 ==================== */

/* 触摸友好的交互优化 */
@media (hover: none) and (pointer: coarse) {
  .nav-step {
    min-height: 44px; /* iOS 推荐的最小触摸目标 */
    min-width: 44px;
  }

  .upload-zone {
    min-height: 120px;
  }

  .cta-buttons button {
    min-height: 48px;
  }

  .setting-group select,
  .setting-group input[type="radio"] {
    min-height: 44px;
  }
}

/* 右侧设备演示 */
.interactive-demo {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.demo-device {
  position: relative;
  max-width: 400px;
  width: 100%;
  perspective: 1000px;
}

.device-frame {
  background: linear-gradient(145deg, #f0f0f0, #cacaca);
  border-radius: 25px;
  padding: 1.5rem;
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.1),
    0 10px 20px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.device-frame:hover {
  transform: translateY(-5px);
  box-shadow:
    0 25px 50px rgba(0, 0, 0, 0.15),
    0 15px 30px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.device-frame::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #d0d0d0, #a0a0a0);
  border-radius: 2px;
  opacity: 0.8;
}

.device-screen {
  background-color: var(--color-background);
  border-radius: 15px;
  min-height: 500px;
  overflow: hidden;
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
}

.device-screen::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 20px;
  background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, transparent 100%);
  border-radius: 15px 15px 0 0;
  pointer-events: none;
}

.demo-screen {
  padding: 1.5rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.demo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 1.5rem;
  position: relative;
}

.demo-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-border), transparent);
}

.demo-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
  position: relative;
}

.demo-title::before {
  content: '';
  position: absolute;
  left: -0.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 1rem;
  background-color: var(--color-primary);
  border-radius: 2px;
}

.demo-progress {
  background-color: var(--color-primary-soft);
  color: var(--color-primary);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.demo-progress::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* 上传演示样式 */
.upload-zone {
  border: 2px dashed var(--color-border);
  border-radius: 12px;
  padding: 3rem 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: var(--color-background-soft);
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
}

.upload-zone::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, transparent 0%, rgba(var(--color-primary-rgb), 0.02) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.upload-zone:hover,
.upload-zone.drag-active {
  border-color: var(--color-primary);
  background-color: var(--color-primary-soft);
  transform: scale(1.02);
}

.upload-zone:hover::before,
.upload-zone.drag-active::before {
  opacity: 1;
}

.upload-zone.drag-active {
  animation: pulse-border 1.5s infinite;
}

@keyframes pulse-border {
  0%, 100% {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 0 rgba(var(--color-primary-rgb), 0.4);
  }
  50% {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 10px rgba(var(--color-primary-rgb), 0);
  }
}

.upload-icon-large {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1rem;
  color: var(--color-primary);
  position: relative;
  transition: transform 0.3s ease;
}

.upload-zone:hover .upload-icon-large {
  transform: scale(1.1);
}

.upload-zone.drag-active .upload-icon-large {
  animation: bounce 0.6s ease-in-out;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.upload-icon-large svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.upload-zone p {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
  transition: color 0.3s ease;
}

.upload-zone:hover p {
  color: var(--color-primary);
}

.supported-formats {
  font-size: 0.8rem;
  color: var(--color-text-soft);
  margin-top: 0.5rem;
  padding: 0.25rem 0.75rem;
  background-color: var(--color-background);
  border-radius: 12px;
  display: inline-block;
  border: 1px solid var(--color-border);
}

.uploaded-files {
  max-height: 200px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) transparent;
}

.uploaded-files::-webkit-scrollbar {
  width: 6px;
}

.uploaded-files::-webkit-scrollbar-track {
  background: transparent;
}

.uploaded-files::-webkit-scrollbar-thumb {
  background-color: var(--color-border);
  border-radius: 3px;
}

.uploaded-files::-webkit-scrollbar-thumb:hover {
  background-color: var(--color-text-soft);
}

.file-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background-color: var(--color-background-soft);
  border-radius: 8px;
  margin-bottom: 0.5rem;
  border: 1px solid var(--color-border);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.file-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, var(--color-primary), var(--color-primary-soft));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.file-item:hover {
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-color: var(--color-primary);
}

.file-item:hover::before {
  opacity: 1;
}

.file-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  width: 2rem;
  text-align: center;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-weight: 500;
  color: var(--color-heading);
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 0.8rem;
  color: var(--color-text-soft);
}

.file-status {
  color: #22c55e;
  font-size: 1.2rem;
  flex-shrink: 0;
  animation: checkmark-appear 0.5s ease-out;
}

@keyframes checkmark-appear {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 设置演示样式 */
.settings-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
}

.setting-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-heading);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.setting-group label::before {
  content: '';
  width: 4px;
  height: 4px;
  background-color: var(--color-primary);
  border-radius: 50%;
  opacity: 0.6;
}

.setting-group select {
  padding: 0.75rem;
  border: 1.5px solid var(--color-border);
  border-radius: 6px;
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 0.9rem;
  transition: all 0.3s ease;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.setting-group select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.1);
}

.setting-group select:hover {
  border-color: var(--color-text-soft);
}

.radio-group {
  display: flex;
  gap: 1rem;
}

.radio-group label {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  transition: all 0.2s ease;
  background-color: var(--color-background);
  position: relative;
  overflow: hidden;
}

.radio-group label::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--color-primary-soft), transparent);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.radio-group label:hover {
  background-color: var(--color-background-soft);
  border-color: var(--color-primary);
  transform: translateY(-1px);
}

.radio-group label:hover::before {
  opacity: 0.1;
}

.radio-group input[type="radio"] {
  margin: 0;
  accent-color: var(--color-primary);
}

.price-preview {
  background-color: var(--color-background-soft);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--color-border);
  position: relative;
  overflow: hidden;
}

.price-preview::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-soft));
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.price-row:hover {
  background-color: var(--color-background);
  margin: 0 -0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}

.price-row.total {
  border-top: 1px solid var(--color-border);
  margin-top: 0.5rem;
  padding-top: 1rem;
  font-weight: 600;
  color: var(--color-primary);
  font-size: 1rem;
}

.price-row.total::before {
  content: '💰';
  margin-right: 0.5rem;
  font-size: 1.1rem;
}

/* 完成演示样式 */
.success-animation {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
  position: relative;
}

.success-animation::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(34, 197, 94, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: success-pulse 2s ease-in-out infinite;
}

@keyframes success-pulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.3;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.1;
  }
}

.checkmark-circle {
  width: 5rem;
  height: 5rem;
  position: relative;
  z-index: 1;
}

.checkmark {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: block;
  stroke-width: 3;
  stroke: #22c55e;
  stroke-miterlimit: 10;
  filter: drop-shadow(0 2px 4px rgba(34, 197, 94, 0.3));
}

.checkmark-circle-path {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 3;
  stroke-miterlimit: 10;
  stroke: #22c55e;
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark-check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}

@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}

.order-summary h4 {
  text-align: center;
  font-size: 1.2rem;
  color: var(--color-heading);
  margin-bottom: 1.5rem;
  position: relative;
}

.order-summary h4::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
}

.pickup-code-demo {
  text-align: center;
  margin-bottom: 1.5rem;
  position: relative;
}

.code-label {
  display: block;
  font-size: 0.9rem;
  color: var(--color-text);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.pickup-code-large {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 2px dashed var(--color-primary);
  display: inline-block;
  position: relative;
  overflow: hidden;
  animation: code-glow 2s ease-in-out infinite alternate;
}

.pickup-code-large::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: code-shine 3s ease-in-out infinite;
}

@keyframes code-glow {
  from {
    box-shadow: 0 0 10px rgba(var(--color-primary-rgb), 0.3);
  }
  to {
    box-shadow: 0 0 20px rgba(var(--color-primary-rgb), 0.6);
  }
}

@keyframes code-shine {
  0% { left: -100%; }
  100% { left: 100%; }
}

.order-details {
  background-color: var(--color-background-soft);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--color-border);
  position: relative;
}

.order-details::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-border), transparent);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.detail-row:hover {
  background-color: var(--color-background);
  margin: 0 -0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}

.detail-row:not(:last-child) {
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0.75rem;
}

/* 底部CTA */
.workflow-cta {
  text-align: center;
  padding: clamp(2rem, 4vw, 3rem);
  background-color: var(--color-background);
  border-radius: 20px;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.cta-description {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: var(--color-text);
  margin-bottom: 2rem;
  font-weight: 500;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.primary-cta {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.secondary-cta {
  background: none;
  border: 2px solid var(--color-border);
  color: var(--color-text);
  padding: 1rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.secondary-cta:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
}

.play-icon {
  color: var(--color-primary);
  font-size: 1.2rem;
}

/* 过渡动画 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.screen-slide-enter-active,
.screen-slide-leave-active {
  transition: all 0.3s ease;
}

.screen-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.screen-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
.sticky-wrapper {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sticky-wrapper > .content-wrapper {
  max-width: 1200px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stepper-container { max-width: 800px; margin: 0 auto 2.5rem auto; width: 100%; }
.step-content {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
}
.step-pane {
  width: 100%;
  max-width: 720px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  max-height: 65vh;
  overflow-y: auto;
  padding: 1.5rem;
}
.step-content h3 { font-size: 1.5rem; font-weight: 600; color: var(--color-heading); margin-bottom: 0.75rem; }
.step-content p { max-width: 500px; color: var(--color-text); margin-bottom: 2rem; }
.mock-uploader {
  width: 35rem;
  height: 20rem;
  border: 2px dashed var(--color-border);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  margin-bottom: 1.25rem;
  margin-top: 1.25rem;
  line-height: 2;
  font-size: 1rem;
}
.mock-uploader .upload-hint {
  font-size: 0.9rem;
  color: var(--color-text-soft);
  margin-top: 0.5rem;
}
.mock-uploader .upload-icon {
  width: 9rem;
  height: 9rem;
  margin-bottom: 0rem;
  color: var(--color-primary);
  padding: auto;

}

/* Transition Styles */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 【重要样式更新】为步骤三的取件信息摘要添加样式 */
.order-summary-container {
  width: 100%;
  max-width: 400px; /* 调整宽度以适应新内容 */
  text-align: left;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-soft);
  overflow: hidden; /* 确保子元素的圆角生效 */
}
.summary-header {
  padding: 1rem 1.5rem;
  font-weight: 600;
  color: var(--color-heading);
  background-color: var(--color-background);
  border-bottom: 1px solid var(--color-border);
}
.summary-body {
  padding: 1.5rem;
}
.pickup-code-wrapper {
  text-align: center;
  margin-bottom: 1.5rem;
}
.pickup-code-label {
  font-size: 0.9rem;
  color: var(--color-text);
}
.pickup-code {
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: 0.2rem;
  color: var(--color-primary);
  background-color: var(--color-background);
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  margin-top: 0.5rem;
  border: 1px dashed var(--color-primary);
}
.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
}
.summary-item.total {
  font-weight: bold;
  font-size: 1.1rem;
  color: var(--color-heading);
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}
.total-price {
  color: var(--color-primary);
  font-size: 1.25rem;
}
/* 【重要样式更新】调整取件信息区域的样式 */
.pickup-info {
  text-align: center; /* 居中显示服务时间 */
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  font-size: 0.9rem;
  color: var(--color-text);
}

.pickup-info p {
  margin: 0; /* 移除默认的段落间距 */
}
.confirm-button {
  width: 100%;
  padding: 0.9rem;
  font-size: 1rem;
  border-radius: 0 0 7px 7px; /* 只保留底部圆角 */
  border-top: 1px solid var(--color-border-hover);
}


/* ==================================================== */
/* 移动端响应式优化                           */
/* ==================================================== */

/* 平板 & 较小桌面 (<= 992px) */
@media (max-width: 992px) {
  .testimonials-grid {
    grid-template-columns: repeat(1, 1fr);
  }

  /* 流程演示平板端优化 */
  .workflow-demo {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .step-explanation {
    order: 1;
    text-align: center;
  }

  .interactive-demo {
    order: 2;
  }

  .demo-device {
    max-width: 400px;
    margin: 0 auto;
  }

  /* 连接线在平板端隐藏，因为步骤是垂直排列的 */
  .connection-line {
    display: none;
  }

  .workflow-navigation {
    flex-direction: column;
    gap: 1.5rem;
  }

  .nav-step {
    width: 100%;
    max-width: 320px;
    flex-direction: row;
    gap: 1rem;
    padding: 1.25rem;
  }

  .step-number {
    margin-bottom: 0;
    flex-shrink: 0;
  }

  .step-label {
    text-align: left;
    white-space: normal;
  }
}

/* 移动设备 (<= 767px) */
@media (max-width: 767px) {
  .content-wrapper {
    padding: 0 1rem;
  }

  .section-title {
    font-size: 1.6rem;
    margin-bottom: 1.5rem;
  }

  .paper-sheet { width: 80%; }
  .keyword-tag { font-size: 0.9rem; padding: 0.4rem 0.8rem; }

  .features-section, .testimonials-section, .faq-section, .cta-section {
    padding: 3rem 1rem;
  }

  .stats-section {
    padding: 2rem 1rem;
  }

  .stat-number {
    font-size: 2rem;
  }

  .stat-label {
    font-size: 0.75rem;
  }

  /* 流程演示移动端优化 */
  .workflow-showcase {
    padding: 2rem 1rem;
  }

  .workflow-header h2 {
    font-size: 1.5rem;
    line-height: 1.3;
  }

  .workflow-header .subtitle {
    font-size: 0.9rem;
    margin-top: 0.5rem;
  }

  .workflow-navigation {
    flex-direction: column;
    gap: 1rem;
    align-items: center;
    margin-bottom: 2rem;
  }

  .nav-step {
    width: 100%;
    max-width: 280px;
    padding: 1rem;
    flex-direction: row;
    gap: 0.75rem;
    background-color: var(--color-background-soft);
    border: 1px solid var(--color-border);
    border-radius: 12px;
    transition: all 0.3s ease;
  }

  .nav-step:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .nav-step.active {
    background-color: var(--color-primary-soft);
    border-color: var(--color-primary);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(var(--color-primary-rgb), 0.2);
  }

  .step-number {
    width: 2.5rem;
    height: 2.5rem;
    font-size: 1rem;
    flex-shrink: 0;
  }

  .step-label {
    font-size: 0.9rem;
    font-weight: 500;
    text-align: left;
    white-space: normal;
    line-height: 1.3;
  }

  .workflow-demo {
    grid-template-columns: 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .step-explanation {
    order: 1;
    text-align: center;
    padding: 1.5rem 1rem;
  }

  .step-explanation h3 {
    font-size: 1.4rem;
    margin-bottom: 1rem;
  }

  .step-explanation p {
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  .feature-highlights {
    flex-direction: column;
    gap: 0.75rem;
    align-items: center;
  }

  .highlight-item {
    justify-content: center;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
  }

  .interactive-demo {
    order: 2;
  }

  .demo-device {
    max-width: 100%;
    width: 100%;
  }

  .device-frame {
    padding: 1rem;
    border-radius: 20px;
    box-shadow:
      0 15px 30px rgba(0, 0, 0, 0.1),
      0 8px 16px rgba(0, 0, 0, 0.05),
      inset 0 1px 0 rgba(255, 255, 255, 0.9);
  }

  .device-screen {
    min-height: 450px;
    border-radius: 12px;
  }

  .demo-screen {
    padding: 1.25rem;
  }

  .demo-header {
    padding-bottom: 0.75rem;
    margin-bottom: 1.25rem;
  }

  .demo-title {
    font-size: 1.1rem;
    font-weight: 600;
  }

  .demo-progress {
    font-size: 0.8rem;
    padding: 0.25rem 0.75rem;
    border-radius: 10px;
  }

  /* 上传演示移动端优化 */
  .upload-zone {
    padding: 2.5rem 1.5rem;
    margin-bottom: 1.25rem;
    border-width: 2px;
    border-radius: 16px;
  }

  .upload-zone:hover,
  .upload-zone.drag-active {
    transform: scale(1.01);
  }

  .upload-icon-large {
    width: 3.5rem;
    height: 3.5rem;
    margin-bottom: 1rem;
  }

  .upload-zone p {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }

  .supported-formats {
    font-size: 0.8rem;
    color: var(--color-text-soft);
  }

  .uploaded-files {
    max-height: 180px;
  }

  .file-item {
    padding: 0.75rem;
    gap: 0.75rem;
    border-radius: 10px;
  }

  .file-icon {
    font-size: 1.4rem;
  }

  .file-name {
    font-size: 0.85rem;
    font-weight: 500;
  }

  .file-size {
    font-size: 0.75rem;
  }

  /* 设置演示移动端优化 */
  .settings-grid {
    gap: 1.25rem;
    margin-bottom: 1.75rem;
  }

  .setting-group {
    gap: 0.6rem;
  }

  .setting-group label {
    font-size: 0.9rem;
    font-weight: 500;
  }

  .setting-group select {
    padding: 0.8rem;
    border-radius: 8px;
    font-size: 0.9rem;
    border-width: 1.5px;
  }

  .radio-group {
    flex-direction: column;
    gap: 0.6rem;
  }

  .radio-group label {
    font-size: 0.9rem;
    padding: 0.5rem;
    border: 1px solid var(--color-border);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .radio-group label:hover {
    background-color: var(--color-background-soft);
    border-color: var(--color-primary);
  }

  .price-preview {
    padding: 1rem;
    border-radius: 10px;
  }

  .price-row {
    font-size: 0.85rem;
    padding: 0.5rem 0;
  }

  /* 完成演示移动端优化 */
  .success-animation {
    margin-bottom: 1.75rem;
  }

  .checkmark-circle {
    width: 4.5rem;
    height: 4.5rem;
  }

  .pickup-code-large {
    font-size: 1.6rem;
    padding: 0.75rem 1.25rem;
    border-radius: 10px;
    letter-spacing: 0.1rem;
  }

  .order-summary h4 {
    font-size: 1.2rem;
    margin-bottom: 1.25rem;
  }

  .order-details {
    padding: 1rem;
    border-radius: 10px;
  }

  .detail-row {
    font-size: 0.85rem;
    padding: 0.5rem 0;
  }

  /* 底部CTA移动端优化 */
  .workflow-cta {
    padding: 2rem 1.5rem;
    border-radius: 18px;
    margin: 0 0.5rem;
  }

  .cta-description {
    font-size: 1.1rem;
    margin-bottom: 1.75rem;
    line-height: 1.5;
  }

  .cta-buttons {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }

  .primary-cta,
  .secondary-cta {
    width: 100%;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    justify-content: center;
    border-radius: 10px;
    min-height: 48px;
  }

  .secondary-cta {
    border-width: 2px;
  }



  .how-it-works-section { height: 250vh; padding: 4rem 1rem 0; }
  .stepper-container { margin-bottom: 1rem; }
  .step-content { padding: 1rem; }
  .step-pane { padding: 1rem; max-height: 70vh; }
  .step-content h3 { font-size: 1.3rem; }
  .step-content p { font-size: 0.85rem; margin: auto; }
  .mock-uploader { height: 10rem; width: 100%; font-size: 0.9rem; }
  .mock-uploader .upload-icon { width: 6rem; height: 6rem; }
  .faq-section h2 { font-size: 1.5rem; }
  .cta-title { font-size: 1.5rem; }
  .cta-description { font-size: 0.9rem; margin-bottom: 1.5rem; }

  /* CTA Logo 移动端优化 */
  .cta-logo {
    margin-bottom: 1.5rem;
  }

  .cta-logo svg {
    width: 48px;
    height: 48px;
  }

  /* BindingGroup 移动端优化 */
  :deep(.binding-group) {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    padding: 0;
    transform: scale(0.9);
    width: 100%;
    max-width: 380px;
  }

  :deep(.binding-group .group-header) {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.8rem 0;
  }

  :deep(.document-item) {
    flex-direction: column;
    align-items: flex-start;
    padding: 0.75rem;
    gap: 0.75rem;
  }

  :deep(.document-item .document-controls) {
    flex-direction: column;
    align-items: stretch;
    width: 100%;
    gap: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--color-border);
  }

  :deep(.document-item .settings-grid) {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }
}

/* 超小屏幕设备 (<= 480px) */
@media (max-width: 480px) {
  .content-wrapper {
    padding: 0 0.75rem;
  }

  .workflow-showcase {
    padding: 1.5rem 0.75rem;
  }

  .workflow-header h2 {
    font-size: 1.4rem;
  }

  .workflow-header .subtitle {
    font-size: 0.85rem;
  }

  .nav-step {
    max-width: 260px;
    padding: 0.875rem;
    gap: 0.6rem;
  }

  .step-number {
    width: 2.25rem;
    height: 2.25rem;
    font-size: 0.9rem;
  }

  .step-label {
    font-size: 0.85rem;
  }

  .step-explanation {
    padding: 1.25rem 0.75rem;
  }

  .step-explanation h3 {
    font-size: 1.3rem;
  }

  .step-explanation p {
    font-size: 0.9rem;
  }

  .device-frame {
    padding: 0.875rem;
    border-radius: 18px;
  }

  .device-screen {
    min-height: 400px;
  }

  .demo-screen {
    padding: 1rem;
  }

  .upload-zone {
    padding: 2rem 1.25rem;
  }

  .upload-icon-large {
    width: 3rem;
    height: 3rem;
  }

  .pickup-code-large {
    font-size: 1.4rem;
    padding: 0.6rem 1rem;
  }

  .cta-buttons {
    gap: 0.75rem;
  }

  .primary-cta,
  .secondary-cta {
    padding: 0.875rem 1.25rem;
    font-size: 0.95rem;
  }

  .workflow-cta {
    padding: 1.75rem 1.25rem;
    margin: 0 0.25rem;
  }
}

/* 横屏模式优化 (landscape) */
@media (max-height: 500px) and (orientation: landscape) {
  .workflow-showcase {
    padding: 1.5rem 1rem;
  }

  .workflow-header {
    margin-bottom: 1.5rem;
  }

  .workflow-header h2 {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
  }

  .workflow-header .subtitle {
    font-size: 0.85rem;
  }

  .workflow-navigation {
    margin-bottom: 1.5rem;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }

  .nav-step {
    max-width: 200px;
    padding: 0.75rem;
    flex-direction: row;
    gap: 0.5rem;
  }

  .step-number {
    width: 2rem;
    height: 2rem;
    font-size: 0.85rem;
  }

  .step-label {
    font-size: 0.8rem;
  }

  .workflow-demo {
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .step-explanation {
    padding: 1rem;
  }

  .step-explanation h3 {
    font-size: 1.2rem;
    margin-bottom: 0.75rem;
  }

  .step-explanation p {
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }

  .device-screen {
    min-height: 350px;
  }

  .demo-screen {
    padding: 0.875rem;
  }

  .upload-zone {
    padding: 1.5rem 1rem;
  }

  .upload-icon-large {
    width: 2.5rem;
    height: 2.5rem;
    margin-bottom: 0.75rem;
  }

  .cta-description {
    margin-bottom: 1.25rem;
    font-size: 1rem;
  }

  .cta-buttons {
    gap: 0.75rem;
  }

  .primary-cta,
  .secondary-cta {
    padding: 0.8rem 1.5rem;
    font-size: 0.9rem;
  }

  .workflow-cta {
    padding: 1.5rem 1.25rem;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .nav-step {
    min-height: 48px;
    min-width: 48px;
  }

  .upload-zone {
    min-height: 120px;
  }

  .cta-buttons button {
    min-height: 48px;
  }

  .setting-group select,
  .setting-group input[type="radio"] {
    min-height: 44px;
  }

  .radio-group label {
    min-height: 44px;
    display: flex;
    align-items: center;
  }

  /* 增加触摸反馈 */
  .nav-step:active {
    transform: scale(0.98);
  }

  .upload-zone:active {
    transform: scale(0.98);
  }

  .cta-buttons button:active {
    transform: scale(0.98);
  }
}

/* 高分辨率屏幕优化 */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .device-frame {
    box-shadow:
      0 20px 40px rgba(0, 0, 0, 0.08),
      0 10px 20px rgba(0, 0, 0, 0.04),
      inset 0 1px 0 rgba(255, 255, 255, 0.95);
  }

  .nav-step.active {
    box-shadow: 0 4px 16px rgba(var(--color-primary-rgb), 0.15);
  }
}
</style>

