<template>
  <div class="home-view container">
    <Teleport to="body">
      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <p class="loading-text">处理中，请稍候...</p>
      </div>
    </Teleport>

    <!-- 登录引导横幅 - 仅对未登录用户显示 -->
    <transition name="slide-down" appear>
      <div v-if="!userStore.isAuthenticated && showLoginGuideBanner" class="login-guide-banner">
        <div class="banner-content">
          <div class="banner-left">
            <div class="banner-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                <polyline points="10,17 15,12 10,7"></polyline>
                <line x1="15" y1="12" x2="3" y2="12"></line>
              </svg>
            </div>
            <div class="banner-text">
              <h3 class="banner-title">登录体验更多功能</h3>
              <p class="banner-subtitle">保存订单历史 • 专属优惠券 • 快速下单</p>
            </div>
          </div>
          <div class="banner-actions">
            <button @click="goToLogin" class="banner-login-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                <polyline points="10,17 15,12 10,7"></polyline>
                <line x1="15" y1="12" x2="3" y2="12"></line>
              </svg>
              立即登录
            </button>
            <button @click="goToRegister" class="banner-register-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="8.5" cy="7" r="4"></circle>
                <line x1="20" y1="8" x2="20" y2="14"></line>
                <line x1="23" y1="11" x2="17" y2="11"></line>
              </svg>
              免费注册
            </button>
            <button @click="remindLater" class="banner-remind-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12,6 12,12 16,14"></polyline>
              </svg>
              稍后提醒
            </button>
          </div>
          <button @click="dismissBanner" class="banner-close-btn" title="关闭提示">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
    </transition>

    <section class="hero-section">
      <h2 class="animated-hero-title">简单、快速、可靠</h2>
      <p>Printerify，为每一次打印赋能。</p>
    </section>

    <section class="process-section">
      <div class="process-card">
        <Stepper :current-step="currentStep" :steps="['配置订单', '支付', '完成']" />

        <div class="step-content">
          <div v-if="currentStep === 1">
            <h3 class="step-title">第一步：上传文档并设置规格</h3>

            <div class="billing-info-trigger" @click="showBillingModal = true">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
              <span>计费规则说明</span>
            </div>

            <div class="upload-notice" v-if="orderStore.groups.length === 0">
              <p><strong>上传须知</strong></p>
              <ul>
                <li><strong>格式推荐</strong>: 为确保打印效果与排版格式一致，强烈建议您上传 <strong>PDF</strong> 格式的文档。</li>
                <li><strong>文件大小</strong>: 单个文件大小建议不超过 <strong>100MB</strong>，最大支持 200MB。大文件上传时间较长，请耐心等待。</li>
                <li><strong>隐私安全</strong>: 所有文件将通过加密通道上传，并存储在专用服务器上。打印完成后，您的文件将被<strong>立即销毁</strong>，绝不外泄。</li>
                <li><strong>合规声明</strong>: 请遵守相关法律法规，<strong>严禁上传</strong>任何涉密、涉政及其他违禁内容的文件。</li>
              </ul>
            </div>

            <FileUploader
              ref="fileUploaderRef"
              @files-selected="handleFilesSelected"
              :disabled="!agreedToTerms || !agreedToPrivacy"
            />

            <transition name="fade">
              <div v-if="orderStore.groups.length > 0 && isBindingHelpVisible" class="binding-help-alert">
                <div class="help-alert-content">
                  <div class="help-alert-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                  </div>
                  <div class="help-alert-text">
                    <strong>装订组使用技巧：</strong>
                    <ul>
                      <li>
                        <strong>合并装订：</strong>新上传时，每个文件都是独立的"装订组"。如需将多个文件装订在一起，请按住组标题旁的 <span>⠿</span> 拖拽，并覆盖到另一组上即可合并。
                      </li>
                      <li>
                        <strong>调整顺序：</strong>当您为合并后的组选择了任意一项装订服务后，组内文件的从上到下顺序即为最终的打印和装订顺序。您可以按住单个文件左侧的 <span>⠿</span> 上下拖拽，自由调整它们的打印顺序。
                      </li>
                    </ul>
                  </div>
                </div>
                <button @click="dismissBindingHelp" class="help-alert-close-btn" title="关闭提示">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
              </div>
            </transition>
            <OrderConfiguration v-if="orderStore.groups.length > 0" />

            <div class="terms-agreement">
              <div>
                <input type="checkbox" id="terms" v-model="agreedToTerms" />
                <label for="terms"> 我已阅读并同意 <a href="#" @click.prevent="showTermsModal = true">《服务条款》</a></label>
              </div>
              <div>
                <input type="checkbox" id="privacy" v-model="agreedToPrivacy" />
                <label for="privacy"> 我已阅读并同意 <a href="#" @click.prevent="showPrivacyModal = true">《隐私协议》</a></label>
              </div>
            </div>

            <BaseButton
              v-if="orderStore.groups.length > 0"
              @click="goToPaymentStep"
              :disabled="!isReadyToGoNext"
              :loading="!orderStore.isReadyToSubmit"
              class="full-width-btn"
              style="margin-top: 2rem;"
            >
              <span>{{ nextStepButtonText }}</span>
            </BaseButton>
          </div>

          <div v-if="currentStep === 2">
            <h3 class="step-title">第二步：确认信息并支付</h3>
            <div v-if="anyEstimated" class="order-estimated-alert" role="alert" aria-live="polite">
              <div class="estimated-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
              </div>
              <div class="estimated-text">
                <strong>价格提示：</strong>
                <span>当前页数为预估，计价可能不准确。建议上传 PDF 格式获得精确价格。若继续提交，系统将尝试在后台更新为精确价格。如有任何疑问，请联系我们。</span>
              </div>
            </div>

            <div class="price-result">
              <p>订单总计</p>
              <p class="price"><strong>¥ {{ totalCost }}</strong></p>
            </div>

            <div class="payment-method-selector">
              <label :class="{ 'active': orderStore.paymentMethod === 'WECHAT' }">
                <input type="radio" v-model="orderStore.paymentMethod" value="WECHAT" name="payment-method"/>
                <img src="/wechat-logo.png" alt="微信支付" class="payment-button-image"/>
              </label>
              <label :class="{ 'active': orderStore.paymentMethod === 'ALIPAY' }">
                <input type="radio" v-model="orderStore.paymentMethod" value="ALIPAY" name="payment-method"/>
                <img src="/alipay-logo.png" alt="支付宝" class="payment-button-image"/>
              </label>
            </div>

            <div class="payment-section">
              <div v-if="orderStore.paymentMethod === 'WECHAT'">
                <p class="payment-instruction">请使用微信扫描下方二维码完成支付</p>
                <img src="/wechat_qr.jpg" alt="微信收款二维码" class="qr-code">
              </div>
              <div v-if="orderStore.paymentMethod === 'ALIPAY'">
                 <p class="payment-instruction">请使用支付宝扫描二维码，或点击下方链接</p>
                 <img src="/alipay_qr.jpg" alt="支付宝收款二维码" class="qr-code">
                 <a href="https://qr.alipay.com/2m611064ovvydd9jbdrnv22" target="_blank" class="payment-link">
                   点此跳转支付宝APP付款
                 </a>
              </div>
            </div>
            <div class="payment-section">
              <PaymentUploader @upload-success="onScreenshotUploaded" />
            </div>
            <div class="form-group">
              <label>请输入手机号以完成下单：</label>
              <input type="tel" v-model="orderStore.phoneNumber" placeholder="用于查询订单" :disabled="isLoading" />
            </div>
            <BaseButton @click="handleCreateOrder" :loading="isLoading" class="full-width-btn">
              我已支付，确认下单
            </BaseButton>
          </div>

          <div v-if="currentStep === 3 && finalOrder" class="completion-view">
            <!-- 【修改】这里的 SVG stroke 颜色使用了 CSS 变量 -->
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="var(--color-success)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            <h3 class="step-title">订单提交成功！</h3>
            <p>取件时请出示取件码，请牢记或截图保存。</p>
            <p>凭手机号和取件码，可在订单查询页面查询订单状态</p>
            <strong> 取件地址：西四学生宿舍 425 </strong>
            <div class="pickup-code-wrapper">
              <span class="pickup-code-label">您的取件码</span>
              <strong class="pickup-code">{{ finalOrder.pickup_code }}</strong>
            </div>
            <p class="order-number-info">完整订单号: {{ finalOrder.order_number }}</p>
            <BaseButton @click="resetForNewOrder" class="full-width-btn">再来一单</BaseButton>
          </div>
        </div>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </section>
  </div>

  <Teleport to="body">
    <Modal :show="showTermsModal" @close="showTermsModal = false">
      <template #header><h3>服务条款</h3></template>
      <template #body>
        <div class="terms-text">
            <p><strong>最后更新日期：2025年7月14日</strong></p>
            <h4>引言与协议接受</h4>
            <p>欢迎使用 Printerify（以下简称"本服务"）。本服务条款构成您（以下简称"用户"）与 Printerify（以下简称"我们"）之间具有法律约束力的协议。在访问或使用本服务之前，请您务必仔细阅读并充分理解本条款的全部内容。您通过访问服务页面、上传文件、下单或任何其他方式使用本服务，即表示您已阅读、理解并同意接受本条款所有内容的约束。若您不同意本条款的任何内容，请立即停止使用本服务。</p>
            <h4>服务描述</h4>
            <p>Printerify 为您提供一个便捷的在线平台，允许您上传需要打印的数字文件，自定义打印规格（如纸张类型、尺寸、颜色等），提交订单，并通过指定的支付方式完成付款。订单完成后，您将获得一个唯一的取件码，凭此码在指定地点领取您的实体打印成品。我们致力于提供高质量的打印服务，但 Printerify 保留根据运营需求随时修改、暂停或永久终止部分或全部服务的权利。若发生此类变动，我们将尽力通过网站公告等形式提前通知用户。</p>
            <h4>用户行为与内容规范</h4>
            <p>用户承诺在使用本服务时，将严格遵守所有适用的法律法规。您对通过本服务上传、提交或分享的所有文件、数据及信息（以下统称为"用户内容"）负有完全的法律责任。您必须保证，您所上传的用户内容拥有合法的知识产权，或已获得相关权利人的充分授权，不会侵犯任何第三方的版权、商标权、专利权、肖像权、隐私权或其他合法权益。严禁用户利用本服务上传、打印或传播任何包含非法、淫秽色情、暴力、恐怖、赌博、诽谤、骚扰、种族歧视或任何其他违反法律、道德及社会公序良俗的内容。Printerify 有权单方面判断用户内容是否违反本条款，并无需通知即可拒绝打印、删除相关内容，并视情节严重程度，暂停或永久终止向该用户提供服务。</p>
            <h4>订单、支付与交付</h4>
            <p>本服务的订单流程、具体价格计算方式以及可接受的支付渠道均以网站页面实时显示为准。您在提交订单前，请仔细核对订单详情，包括打印规格、数量和总金额。订单一旦提交，即表示您确认了订单内容。Printerify 将根据您上传的支付凭证来核实付款状态，并在确认付款后开始处理您的订单。我们会尽力确保打印质量，但由于设备、耗材及文件本身等因素，打印成品可能存在合理的色彩、尺寸误差，此不属于质量问题。若因 Printerify 的设备或操作失误导致严重的打印质量问题，我们将根据具体情况为您提供重印或退款服务。订单完成后生成的取件码是您领取打印成品的唯一凭证，请务必妥善保管，因您个人保管不善导致的任何损失，由您自行承担。</p>
            <h4>知识产权</h4>
            <p>Printerify 尊重并保护知识产权。您上传至本服务的用户内容的知识产权，仍归您或原始权利人所有。您仅授予我们一项非独家的、为履行打印订单之目的所必需的权利，来使用、复制和处理您的用户内容。订单履行完毕后，此授权自动终止。与此同时，Printerify 网站本身所包含的所有内容，包括但不限于Logo、商标、文字、图形、界面设计、代码、算法和软件的知识产权，均归我们所有，受相关法律保护。未经我们书面许可，任何个人或组织不得以任何形式进行复制、修改、传播或用于任何商业目的。</p>
            <h4>免责声明与责任限制</h4>
            <p>在适用法律允许的最大范围内，本服务及其所有内容均是"按现状"和"按可用状态"提供的，Printerify 不作任何形式的明示或暗示的保证，包括但不限于服务的稳定性、可靠性、准确性或特定用途的适用性。对于因不可抗力、第三方服务（如网络中断）、系统维护或用户自身原因（如上传了格式错误、内容有误、分辨率过低的文件）导致的任何服务中断或打印质量问题，我们不承担责任。在任何情况下，我们因履行本条款而产生的全部赔偿责任，累计总额不应超过您为引起该责任的特定订单所支付的费用总额。</p>
            <h4>协议的终止</h4>
            <p>如果用户违反本服务条款中的任何规定，Printerify 有权随时单方面中断或终止向该用户提供服务，而无需事先通知。用户也可以随时停止使用本服务，以终止本协议。协议终止后，我们不再有义务为用户提供任何服务，但用户在使用服务期间应尽的义务（如保密、知识产权、赔偿等）不因协议终止而免除。</p>
            <h4>条款的修订</h4>
            <p>我们保留根据业务发展和法律法规变化，不时修订本服务条款的权利。条款更新后，我们将在网站的显著位置发布公告，以通知用户。修订后的条款自发布之日起生效。若您在条款修订后继续使用 Printerify 的服务，即表示您已接受并同意遵守更新后的条款。</p>
            <h4>法律适用与争议解决</h4>
            <p>本条款的订立、生效、解释、履行及争议解决，均适用中华人民共和国（不含港澳台地区）的法律。因本条款产生的或与本条款有关的任何争议，双方应首先尝试通过友好协商解决。如果协商不成，任何一方均有权将争议提交至 Printerify 服务提供方所在地有管辖权的人民法院通过诉讼解决。</p>
        </div>
      </template>
    </Modal>

    <Modal :show="showPrivacyModal" @close="showPrivacyModal = false">
      <template #header><h3>隐私协议</h3></template>
      <template #body>
        <div class="terms-text">
            <p><strong>最后更新日期：2025年7月14日</strong></p>
            <h4>引言</h4>
            <p>Printerify（以下简称"我们"）深知个人信息对您的重要性，并承诺将依据法律法规，采取严格的安全保护措施，全力保护您的个人信息及隐私安全。本隐私协议旨在向您清晰地说明，在您使用我们的在线打印服务过程中，Printerify 如何收集、使用、存储、共享和保护您的个人信息，以及您所享有的相关权利。请您在使用本服务前，仔细阅读并确认您已经充分理解本协议所写明的内容。</p>
            <h4>我们收集的信息类型</h4>
            <p>为了向您提供完整、优质的打印服务，Printerify 会根据合法、正当、必要的原则，收集以下与您相关的信息。首先，是您为履行订单而主动提供的个人身份与联络信息，主要指您的手机号码，我们将用其与您进行订单相关的沟通。其次，是您为实现打印目的而上传的用户内容，即您希望打印的数字文件（如PDF、Word文档、图片等）。再次，当您选择特定支付方式时，我们可能会收集您上传的支付凭证截图，用以核实您的付款状态。最后，为了维护和改进我们的服务，Printerify 可能会自动收集一些技术与日志信息，例如您的IP地址、浏览器类型、操作系统、访问服务的日期与时间，以及您的操作记录等。这些信息通常是匿名的，无法直接关联到您的个人身份。</p>
            <h4>我们如何使用您的信息</h4>
            <p>Printerify 严格遵守法律法规的规定及与您的约定，将收集到的信息用于以下明确、具体的目的。最主要的使用目的是履行您的打印订单，我们会处理您上传的文件并使用您的手机号码，以便在订单状态变更（如打印完成、可供取件）时与您取得联系。同时，我们会使用您的支付凭证来确认订单款项是否到账，以启动订单处理流程。此外，我们会对收集到的匿名化技术与日志信息进行分析，用于监控服务运行状态、排查故障、优化网站性能和用户体验，从而为您提供更稳定、更便捷的服务。</p>
            <h4>信息的共享与披露</h4>
            <p>我们对您的信息负有保密义务，并承诺绝不会将您的个人信息或您上传的打印文件出售、出租或以任何其他形式与任何无关的第三方进行交易。我们仅在以下少数、必要的情况下，才会共享或披露您的信息。一是为实现打印目的，我们可能会将您的文件提供给 Printerify 内部负责打印操作的人员。二是在获得您明确、单独的同意后，我们可能会在您同意的范围内共享信息。三是根据适用的法律法规、法律程序的要求、强制性的行政或司法要求，我们可能有义务对外提供您的信息。在符合法律法规的前提下，当我们收到上述披露信息的请求时，会要求对方必须出具与之相应的法律文件。</p>
            <h4>数据安全</h4>
            <p>Printerify 已采取了符合业界标准、合理可行的物理、技术及行政管理上的安全措施，来保护您提供的信息，防止数据遭到未经授权的访问、公开披露、使用、修改、损坏或丢失。例如，我们使用SSL加密技术对数据传输过程进行保护；我们部署了严格的访问控制机制，确保只有授权人员才可访问个人信息；我们会举办安全和隐私保护培训课程，加强员工对于保护信息重要性的认识。尽管我们已采取上述措施，但请您理解，由于技术的限制以及可能存在的各种恶意手段，在互联网行业，不可能始终保证信息百分之百的安全。</p>
            <h4>数据保留</h4>
            <p>我们只在为实现本协议所述目的所必需的期限内，以及法律法规所要求的时限内保留您的个人信息。对于您为打印而上传的文件及支付凭证，Printerify 承诺，在您的订单完成（即您成功取件或订单关闭）后的30天内，将从我们的服务器上进行永久性、不可恢复的删除，以最大限度地保护您的隐私。您的订单记录及关联的手机号码等信息，将为遵守相关法律规定（如电子商务法）及处理潜在纠纷的需要，保留更长的时间。</p>
            <h4>用户的权利</h4>
            <p>根据相关法律法规，我们保障您对自己的个人信息行使以下权利：您有权访问、更正或补充您的信息。考虑到本服务的性质，您对上传文件的主要管理权限体现在下单前的修改与删除。对于您的个人信息，如需行使访问、更正或请求删除的权利，您可以通过我们提供的联系方式与 Printerify 沟通。在核实您的身份后，我们将响应您的请求。</p>
            <h4>儿童隐私</h4>
            <p>我们的服务主要面向成年人。Printerify 不会在知情的情况下，收集未满14周岁（或您所在司法辖区规定的其他年龄）儿童的个人信息。如果我们发现自己在无意中收集了儿童的个人信息，我们会设法尽快删除相关数据。</p>
            <h4>协议的更新</h4>
            <p>Printerify 的隐私协议可能会根据服务的变更和法律法规的要求适时进行更新。未经您明确同意，我们不会削减您按照本隐私协议所应享有的权利。任何更新我们都会在网站上发布修订后的版本，并以公告形式通知您。对于重大变更，我们还会提供更为显著的通知。</p>
            <h4>联系我们</h4>
            <p>如果您对本隐私协议有任何疑问、意见或建议，或者希望行使您的用户权利，欢迎随时通过以下方式与我们联系：</p>
            <p>电子邮箱：xicheng.lin@foxmail.com</p>
            <p>我们将尽快审核所涉问题，并在验证您的用户身份后的十五个工作日内予以回复。</p>
        </div>
      </template>
    </Modal>

    <Modal :show="showBillingModal" @close="showBillingModal = false">
      <template #header><h3>计费规则说明</h3></template>
      <template #body>
        <div class="billing-rules-content">
          <li>
            <strong>计价公式</strong>
          <p><span class="formula-highlight">总费用 = 基础服务费 + 打印费用 + 装订费用（可选）</span></p>
          </li>
          <ul>
            <li>
              <strong>基础服务费</strong>
              <p>每笔订单将统一收取 0.50元 的基础服务费，用于覆盖设备维护和系统运营成本。</p>
            </li>
            <li>
              <strong>打印费用</strong>
              <p>单面双面相同价格。</p>
              <p>根据您选择的规格（纸张规格、色彩、单双面）按页计费，具体单价以页面实时显示为准。</p>
              <table class="price-table">
                <thead>
                  <tr>
                    <th>规格</th>
                    <th>克重</th>
                    <th>色彩</th>
                    <th>单价（每面）</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>A4</td>
                    <td>70g</td>
                    <td>黑白</td>
                    <td>0.15元</td>
                  </tr>
                  <tr>
                    <td>A4</td>
                    <td>80g</td>
                    <td>黑白</td>
                    <td>0.15元</td>
                  </tr>
                  <tr>
                    <td>B5</td>
                    <td>70g</td>
                    <td>黑白</td>
                    <td>0.12元</td>
                  </tr>
                </tbody>
              </table>
              </li>

            <li>
              <strong>装订费用</strong>
              <p>若您选择装订服务，将根据不同的装订方式额外收取固定费用。</p>
            </li>
          </ul>
        </div>
      </template>
    </Modal>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onUnmounted, onMounted } from 'vue'; //【修改】引入computed, watch, onUnmounted
import { useRouter } from 'vue-router'; // 导入路由
import { useOrderStore } from '@/stores/order';
import apiService from '@/services/apiService'; //【修改】使用apiService而不是直接使用axios
import { useUserStore } from '@/stores/user'; // 导入用户状态管理

// 导入组件
import Stepper from '@/components/Stepper.vue';
import FileUploader from '@/components/FileUploader.vue';
import PaymentUploader from '@/components/PaymentUploader.vue';
import BaseButton from '@/components/BaseButton.vue';
import Modal from '@/components/Modal.vue';
import OrderConfiguration from '@/components/OrderConfiguration.vue';

// --- 使用 Pinia Store 和 Router ---
const orderStore = useOrderStore();
const userStore = useUserStore(); // 使用用户状态管理
const router = useRouter(); // 使用路由
const screenshotId = ref(null); // <-- 【新增】用于存储凭证ID的状态

// --- UI 控制相关的本地状态 ---
const currentStep = ref(1);
const isLoading = ref(false); // 用于控制加载状态
const errorMessage = ref('');
const agreedToTerms = ref(false);
const agreedToPrivacy = ref(false);
const showTermsModal = ref(false);
const showPrivacyModal = ref(false);
const showBillingModal = ref(false); // 用于显示计费规则说明的模态框
const fileUploaderRef = ref(null);
const finalOrder = ref(null); // 用于存储最终成功创建的订单信息

// ▼▼▼ 在这里新增控制逻辑 ▼▼▼
const isBindingHelpVisible = ref(true); // 默认显示

function dismissBindingHelp() {
  isBindingHelpVisible.value = false;
}

// 登录引导横幅相关状态
const showLoginGuideBanner = ref(true); // 默认显示

// 页面初始化时检查用户是否之前关闭过横幅
onMounted(() => {
  // 移除本地存储检查，让横幅每次都能显示
  // const hideBanner = localStorage.getItem('hideLoginGuideBanner');
  // if (hideBanner === 'true') {
  //   showLoginGuideBanner.value = false;
  // }
});

// 监听用户登录状态变化
const unwatchAuth = watch(() => userStore.isAuthenticated, (isAuth) => {
  if (isAuth) {
    // 用户登录成功后自动隐藏横幅
    showLoginGuideBanner.value = false;
  } else {
    // 用户登出后重新显示横幅
    showLoginGuideBanner.value = true;
  }
});

// 组件卸载时清理监听器
onUnmounted(() => {
  unwatchAuth();
});

function dismissBanner() {
  showLoginGuideBanner.value = false;
  // 不再保存到本地存储，让横幅在下次访问时重新显示
  // localStorage.setItem('hideLoginGuideBanner', 'true');
}

function goToLogin() {
  // 跳转到登录页面
  router.push('/auth/login');
  dismissBanner();
}

function goToRegister() {
  // 跳转到注册页面
  router.push('/auth/register');
  dismissBanner();
}

function remindLater() {
  // 稍后提醒逻辑，隐藏横幅一段时间后重新显示
  showLoginGuideBanner.value = false;
  // 设置一个较短的延迟时间，比如5分钟后重新显示
  setTimeout(() => {
    if (!userStore.isAuthenticated) {
      showLoginGuideBanner.value = true;
    }
  }, 5 * 60 * 1000); // 5分钟
}
// ▲▲▲ 新增代码结束 ▲▲▲

const isReadyToGoNext = computed(() => {
  return orderStore.isReadyToSubmit && agreedToTerms.value && agreedToPrivacy.value;
});

// 【新增】这个计算属性根据不同状态显示不同的按钮文本
const nextStepButtonText = computed(() => {
  if (!agreedToTerms.value || !agreedToPrivacy.value) {
    return '请先同意服务条款和隐私协议';
  }
  if (!orderStore.isReadyToSubmit) {
    return '处理文件中...';
  }
  return `下一步，确认订单 (总计 ¥${totalCost.value})`;
});

const totalCost = computed(() => orderStore.totalCost);

// --- 方法 ---
function handleFilesSelected(files) {
  orderStore.addFiles(files);
}

// 【新增】处理截图上传成功的事件函数
function onScreenshotUploaded(uploadedId) {
  screenshotId.value = uploadedId;
}

function goToPaymentStep() {
  if (isReadyToGoNext.value) { // <--- 将 isReadyToSubmit 修改为 isReadyToGoNext
    currentStep.value = 2;
  }
}

// 【关键】最终的订单创建函数
async function handleCreateOrder() {
  // 基础校验
  if (!screenshotId.value) { // <-- 【修改】校验逻辑
    errorMessage.value = '请先上传付款截图！';
    return;
  }
  if (!orderStore.phoneNumber) {
    errorMessage.value = '请输入您的手机号码！';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  // 1. 从 Store 中构建后端需要的JSON数据结构
  const payload = {
    // 【修改】将 screenshotId 添加到 payload 中
    payment_screenshot_id: screenshotId.value,
    payment_method: orderStore.paymentMethod, // <-- 【新增】确保这一行存在
    phone_number: orderStore.phoneNumber,
    groups: orderStore.groups.map((group, groupIndex) => ({
      binding_type: group.bindingType,
      sequence_in_order: groupIndex + 1,
      documents: group.documents.map((doc, docIndex) => ({
        file_id: doc.serverId, // 使用预上传后服务器返回的ID
        original_filename: doc.fileName,
        paper_size: doc.settings.paperSize, // <--- 【核心修正】在这里补上 paper_size 字段
        color_mode: doc.settings.colorMode,
        print_sided: doc.settings.printSided,
        copies: doc.settings.copies,
        sequence_in_group: docIndex + 1,
      })),
    })),
    // payment_method: orderStore.paymentMethod,
    // 【待办】支付凭证也需要预上传并获取ID
  };

  try {
    // 2. 发送创建订单的POST请求
    const response = await apiService.createOrder(payload);

    // 3. 处理成功响应
    finalOrder.value = response.data; // 保存成功返回的订单数据
    currentStep.value = 3; // 跳转到成功页面

  } catch (error) {
    console.error('Order creation failed:', error.response?.data || error.message);
    errorMessage.value = '订单创建失败，请稍后重试或联系客服。';
  } finally {
    isLoading.value = false;
  }
}

function resetForNewOrder() { // <--- 1. 将函数名从 reset 修改为 resetForNewOrder
  orderStore.resetStore();
  currentStep.value = 1;
  finalOrder.value = null; // <--- 2. 增加这一行，清空上一单的结果
  agreedToTerms.value = false;
  agreedToPrivacy.value = false;
  errorMessage.value = '';
  screenshotId.value = null; // <--- 3. 增加这一行，重置截图ID
  if (fileUploaderRef.value) {
    fileUploaderRef.value.reset();
  }
}

// 订单层面的“是否预估”判断（任一文档为预估即为预估）
const anyEstimated = computed(() => orderStore.groups.some(g => g.documents.some(d => d.isEstimated)));

</script>

<style scoped>

/* ===================================================================
  样式已更新，使用 CSS 变量以支持主题切换。
  所有布局、尺寸和响应式逻辑均已完整保留。
  ===================================================================
*/
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.hero-section {
  text-align: center;
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.hero-section h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-heading); /* 已修改 */
  margin-bottom: 0.5rem;
}

.hero-section p {
  font-size: 1.125rem;
  color: var(--color-text-mute); /* 已修改 */
}

.process-section {
  padding-bottom: 2rem;
}

/* 统一风格：订单层级的预估提示样式（与帮助提示风格一致） */
.order-estimated-alert {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.08);
  border: 1px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
  border-radius: 12px;
  margin: 0.5rem 0 1rem;
}

.order-estimated-alert .estimated-icon {
  color: var(--color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}

.order-estimated-alert .estimated-text strong {
  display: block;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.25rem;
}

.order-estimated-alert .estimated-text span {
  color: var(--color-text);
  font-size: 0.95rem;
  line-height: 1.6;
}

.process-card {
  background-color: var(--color-background-soft); /* 已修改 */
  border-radius: 16px;
  padding: 1.5rem 2.5rem;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: var(--shadow-card); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
  transition: background-color 0.3s, border-color 0.3s;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 2rem;
  color: var(--color-heading); /* 已修改 */
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.options-grid div {
  display: flex;
  flex-direction: column;
}

.options-grid label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--color-heading); /* 已修改 */
}

.price-result {
  background-color: var(--color-background-mute); /* 已修改 */
  border: 1px solid var(--color-primary); /* 已修改 */
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  text-align: center;
}

.price-result p {
    color: var(--color-text);
}

.price {
  font-size: 1.75rem;
  color: var(--color-primary); /* 已修改 */
  font-weight: 700;
}

.payment-section {
  border-top: 1px solid var(--color-border); /* 已修改 */
  padding: 1.5rem 0;
  margin-top: 1.5rem;
  text-align: center;
}

.payment-instruction {
  margin-top: 0;
  color: var(--color-text); /* 已修改 */
}

.qr-code {
  max-width: 180px;
  margin: 1rem auto;
  display: block;
  border-radius: 8px;
  background-color: white; /* 为确保二维码可扫，背景强制为白色 */
  padding: 5px; /* 增加内边距，确保扫描效果 */
}

.form-group {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block; /* 【修复】让标签独占一行，从而与输入框产生间距 */
  margin-bottom: 0.75rem; /* 【修复】增加明确的下边距 */
  font-weight: 500;
  color: var(--color-heading);
}

.full-width-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1.1rem;
}

.completion-view {
  text-align: center;
  padding: 2rem 0;
}

.completion-view > p {
  color: var(--color-text-mute); /* 已修改 */
  margin-bottom: 1rem;
}

.pickup-code-wrapper {
  background-color: var(--color-background-mute); /* 已修改 */
  border: 1px dashed var(--color-primary); /* 已修改 */
  padding: 1rem;
  border-radius: 8px;
  margin: 1.5rem auto;
  max-width: 300px;
}

.pickup-code-label {
  font-size: 1rem;
  color: var(--color-text); /* 已修改 */
}

.pickup-code {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary); /* 已修改 */
  letter-spacing: 4px;
  margin-top: 0.5rem;
}

.error-message {
  color: var(--color-text-on-danger); /* 已修改 */
  font-weight: 500;
  margin-top: 1.5rem;
  text-align: center;
  background-color: var(--color-danger); /* 已修改 */
  padding: 0.75rem;
  border-radius: 8px;
}

.order-number-info {
  color: var(--color-text-mute); /* 已修改 */
  font-size: 0.875rem;
  margin-top: -0.5rem;
  margin-bottom: 2rem;
}

.upload-notice {
  background-color: var(--color-background-mute);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: var(--color-text);
}

.upload-notice p {
  margin: 0 0 0.75rem 0;
  font-weight: 500;
  color: var(--color-heading);
}
/* --- 【新增】请在这里添加以下新规则 --- */
.upload-notice p strong {
  font-weight: 700; /* 或者 bold, 800, 900，具体取决于字体支持 */
}

.upload-notice ul {
  list-style-type: none;
  padding-left: 0;
}

.upload-notice li {
  margin-bottom: 0.75rem; /* 稍微增加行间距 */
  position: relative;
  padding-left: 1.25rem;
  font-weight: 500; /* 【修复】恢复字体粗细 */
  line-height: 1.6; /* 增加行高，提升可读性 */
}

.upload-notice li::before {
  content: '•';
  color: var(--color-primary);
  font-weight: bold;
  display: inline-block;
  position: absolute;
  left: 0;
  top: 0;
}

.upload-notice li:last-child {
  margin-bottom: 0;
}

.upload-notice li strong {
  color: var(--color-primary); /* 【修复】将关键词颜色修正为主题蓝 */
  font-weight: 600; /* 【修复】恢复关键词粗细 */
}

.payment-method-selector {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.payment-method-selector label {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 4px;
  transition: all 0.2s ease-in-out;
  width: 160px;
  height: 56px;
  box-sizing: border-box;
  background-color: var(--color-background);
}

.payment-method-selector label:hover {
  border-color: var(--color-border-hover);
}

.payment-method-selector label.active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px var(--color-primary);
}

.payment-method-selector input[type="radio"] {
  display: none;
}

.payment-button-image {
  display: block;
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
  transition: filter 0.3s; /* 【新增】为滤镜添加平滑过渡 */
}

/* --- 【核心修改】暗色模式下，为图片应用滤镜 --- */
html.dark .payment-button-image {
  filter: invert(1) grayscale(1) brightness(1.5);
}

.payment-link {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: #1677ff; /* 支付宝品牌色，保持不变 */
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.payment-link:hover {
  background-color: #4096ff;
}

.terms-agreement {
  font-size: 0.9rem;
  color: var(--color-text-mute); /* 已修改 */
  margin-top: 2rem;
  margin-bottom: 0;
  padding: 1rem;
  background-color: var(--color-background-mute); /* 已修改 */
  border: 1px solid var(--color-border); /* 已修改 */
  border-radius: 8px;
}

.terms-agreement div {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.terms-agreement div:last-child {
  margin-bottom: 0;
}

.terms-agreement input[type="checkbox"] {
  margin-right: 0.5rem;
  width: auto;
}

.terms-agreement label {
  margin-bottom: 0;
  font-weight: normal;
}

.terms-agreement a {
  color: var(--color-primary); /* 已修改 */
  text-decoration: underline;
  cursor: pointer;
}

.terms-text {
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.7;
  text-align: left;
  color: var(--color-text); /* 已修改 */
}

.terms-text h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  color: var(--color-heading); /* 已修改 */
}

.terms-text p {
  margin-bottom: 1em;
}

.terms-text p:first-child {
    margin-top: 0;
}

.billing-info-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--color-text-mute); /* 已修改 */
  font-size: 0.9rem;
  margin-bottom: 2rem;
  cursor: pointer;
  transition: color 0.2s;
}

.billing-info-trigger:hover {
  color: var(--color-primary); /* 已修改 */
}

.billing-info-trigger svg {
  margin-top: -2px;
}

.billing-rules-content ul {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.billing-rules-content li {
  margin-bottom: 1.25rem;
}

.billing-rules-content li:last-child {
  margin-bottom: 0;
}

.billing-rules-content strong {
  display: block;
  font-size: 1.1em;
  color: var(--color-heading); /* 已修改 */
  margin-bottom: 0.25rem;
}

.billing-rules-content p {
  margin: 0;
  color: var(--color-text-mute); /* 已修改 */
  line-height: 1.6;
}

.formula-highlight {
  display: block;
  text-align: center;
  margin: 1.2em auto 1.2em auto;
  background: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 350;
  padding: 0.8em 1.2em;
  border-radius: 6px;
  font-size: 1.12em;
  letter-spacing: 0.5px;
}
/* 响应式优化 formula-highlight */
.formula-highlight {
  display: block;
  text-align: center;
  margin: 1.2em auto;
  background: var(--color-background-mute);
  color: var(--color-text);
  font-weight: 350;
  padding: 0.8em 1.2em;
  border-radius: 6px;
  font-size: 1.12em;
  letter-spacing: 0.5px;
  word-break: break-word;
  max-width: 100%;
  box-sizing: border-box;
}

@media (max-width: 600px) {
  .formula-highlight {
    font-size: 1em;
    padding: 0.7em 0.5em;
    margin: 1em 0.2em;
  }
}

/* 响应式优化 price-table */
.price-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5em;
  font-size: 0.95em;
  overflow-x: auto;
  display: block;
}

.price-table th, .price-table td {
  border: 1px solid var(--color-border);
  padding: 0.5em 1em;
  text-align: center;
  min-width: 80px;
}

@media (max-width: 600px) {
  .price-table {
    font-size: 0.85em;
    margin-top: 0.5em;
    /* 让表格横向滚动，防止内容溢出 */
    overflow-x: auto;
    display: block;
  }
  .price-table th, .price-table td {
    padding: 0.4em 0.5em;
    min-width: 70px;
    font-size: 0.95em;
  }
}

.price-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5em;
  font-size: 0.95em;
}
.price-table th, .price-table td {
  border: 1px solid var(--color-border);
  padding: 0.5em 1em;
  text-align: center;
}
.price-table th {
  background: var(--color-background-mute);
  font-weight: 600;
  color: var(--color-text);
}
.price-table tr:nth-child(even) {
  background: var(--color-background);
}

html.dark .price-table th {
  background: var(--color-background-mute);
  color: var(--color-text);
}
html.dark .price-table td {
  border-color: var(--color-border);
  color: var(--color-text);
}
html.dark .price-table tr:nth-child(even) {
  background: var(--color-background);
}

@media (max-width: 767px) {
  .hero-section h2 { font-size: 2rem; }
  .hero-section p { font-size: 1rem; }
  .step-title { font-size: 1.25rem; }
  .process-card { padding: 1.5rem 1rem; }
  .pickup-code { font-size: 2rem; }
  .payment-method-selector { gap: 1rem; }
  .payment-method-selector label { width: 140px; height: 48px; }
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(var(--color-background-rgb, 255, 255, 255), 0.8); /* 已修改，支持主题 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2); /* 已修改，支持主题 */
  border-top-color: var(--color-primary); /* 已修改 */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text); /* 已修改 */
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
/* --- 【修复】为手机号输入框添加样式 --- */
.form-group input[type="tel"] {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input[type="tel"]:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

.form-group input[type="tel"]::placeholder {
  color: var(--color-text-mute);
  opacity: 0.7;
}
/* ▼▼▼ 在这里新增全局帮助信息框的样式 ▼▼▼ */
.binding-help-alert {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  /* 定义一个更柔和的信息提示背景色 */
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.08);
  border: 1px solid rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
  border-radius: 12px;
  padding: 1rem;
  margin-top: 2rem; /* 与上方的 FileUploader 保持间距 */
  margin-bottom: 1.5rem; /* 与下方的 OrderConfiguration 保持间距 */
}

.help-alert-content {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.help-alert-icon {
  color: var(--color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}


.help-alert-close-btn {
  background: none;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-mute);
  transition: background-color 0.2s, color 0.2s;
  flex-shrink: 0;
}

.help-alert-close-btn:hover {
  background-color: var(--color-background-mute);
  color: var(--color-text);
}
/* 更新帮助文本的样式 */
.help-alert-text strong {
  font-weight: 600;
  color: var(--color-heading);
  display: block; /* 让标题独占一行 */
  margin-bottom: 0.5rem;
}

.help-alert-text p,
.help-alert-text ul { /* 同时为 p 和 ul 设置样式 */
  font-size: 0.9rem;
  color: var(--color-text);
  margin: 0;
  line-height: 1.6;
  padding-left: 0.1em; /* 为 ul 添加左边距 */
}

.help-alert-text li {
  margin-bottom: 0.5rem;
}
.help-alert-text li:last-child {
  margin-bottom: 0;
  padding-left: 0; /* 最后一项不需要左边距 */
}

.help-alert-text li::marker {
  color: var(--color-primary); /* 美化列表的项目符号 */
}

.help-alert-text li strong {
  display: inline; /* 修正 li 内 strong 的显示方式 */
  margin-bottom: 0;
}

/* 这个是新增的，用于高亮显示拖拽图标 */
.help-alert-text span {
  font-family: monospace;
  background-color: var(--color-border);
  padding: 0 4px;
  border-radius: 3px;
  font-weight: 600;
  display: inline-block;
  line-height: 1;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
/* ▲▲▲ 新增样式结束 ▲▲▲ */

/* ===================================================================
   登录引导横幅样式
   =================================================================== */
.login-guide-banner {
  background: linear-gradient(135deg,
    rgba(248, 250, 252, 0.95) 0%,
    rgba(241, 245, 249, 0.9) 100%);
  border-radius: 16px;
  margin-bottom: 2rem;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  overflow: hidden;
  position: relative;
}

.banner-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  gap: 1.5rem;
  position: relative;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.banner-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  color: var(--color-primary);
  flex-shrink: 0;
}

.banner-text {
  color: var(--color-heading);
}

.banner-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  line-height: 1.2;
}

.banner-subtitle {
  font-size: 0.9rem;
  margin: 0;
  color: var(--color-text-mute);
  line-height: 1.4;
}

.banner-actions {
  display: flex;
  gap: 0.75rem;
  flex-shrink: 0;
}

.banner-login-btn,
.banner-register-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.banner-login-btn {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.banner-login-btn:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
}

.banner-register-btn {
  background: var(--color-primary);
  color: white;
}

.banner-register-btn:hover {
  background: rgba(59, 130, 246, 0.9);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.banner-remind-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  background: rgba(148, 163, 184, 0.1);
  color: var(--color-text-mute);
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.banner-remind-btn:hover {
  background: rgba(148, 163, 184, 0.15);
  border-color: rgba(148, 163, 184, 0.3);
  transform: translateY(-1px);
}

.banner-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(148, 163, 184, 0.1);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-mute);
  transition: all 0.2s ease;
  opacity: 0.7;
}

.banner-close-btn:hover {
  background: rgba(148, 163, 184, 0.2);
  opacity: 1;
  transform: scale(1.1);
}

/* 横幅动画 */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .banner-content {
    padding: 1.25rem 1.5rem;
    gap: 1rem;
  }

  .banner-title {
    font-size: 1.125rem;
  }

  .banner-subtitle {
    font-size: 0.85rem;
  }
}

@media (max-width: 768px) {
  .banner-content {
    flex-direction: column;
    align-items: stretch;
    padding: 1.25rem 1.25rem 1rem;
    gap: 1.25rem;
  }

  .banner-left {
    justify-content: center;
    text-align: center;
  }

  .banner-actions {
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .banner-close-btn {
    top: 0.75rem;
    right: 0.75rem;
  }

  .banner-title {
    font-size: 1.1rem;
  }

  .banner-subtitle {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .login-guide-banner {
    margin-bottom: 1.5rem;
    border-radius: 12px;
  }

  .banner-content {
    padding: 1rem 1rem 0.75rem;
  }

  .banner-actions {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }

  .banner-login-btn,
  .banner-register-btn,
  .banner-remind-btn {
    width: 100%;
    justify-content: center;
    padding: 0.875rem 1rem;
  }

  .banner-left {
    gap: 0.75rem;
  }

  .banner-icon {
    width: 40px;
    height: 40px;
  }

  .banner-title {
    font-size: 1rem;
  }

  .banner-subtitle {
    font-size: 0.75rem;
  }
}

/* 暗色模式适配 */
html.dark .login-guide-banner {
  background: linear-gradient(135deg,
    rgba(30, 41, 59, 0.95) 0%,
    rgba(51, 65, 85, 0.9) 100%);
  border-color: rgba(148, 163, 184, 0.3);
}

/* ===================================================================
   登录引导横幅样式结束
   =================================================================== */

/* ---【优化方案】基于 CSS 变量的真正无缝循环动画 --- */

/* 1. 基础/暗色模式样式 */
.animated-hero-title {
  /* ▼▼▼【核心修改 ①】定义一个 CSS 变量，用于控制背景宽度 ▼▼▼ */
  --scroll-width: 400px;

  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 3.2rem;
  text-align: center;
  letter-spacing: -1.5px;

  background: linear-gradient(
    100deg,
    #666666, #b2b2b2, #ffffff, #b2b2b2, #666666
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;

  background-repeat: repeat-x;

  /* ▼▼▼【核心修改 ②】使用变量设定背景尺寸 ▼▼▼ */
  background-size: var(--scroll-width) 100%;

  /* 应用下方经过优化的、动态的滚动动画 */
  animation: seamless-scroll 5s linear infinite;

  text-shadow:
    0px 1px 1px rgba(255, 255, 255, 0.1),
    0 0 10px rgba(192, 219, 255, 0.2),
    0 0 30px rgba(192, 219, 255, 0.1),
    0px -1px 1px rgba(0, 0, 0, 0.4);
}

/* 2. 亮色模式专属样式 */
html:not(.dark) .animated-hero-title {
  /* ▼▼▼【核心修改 ③】仅需重写变量的值，即可改变背景尺寸 ▼▼▼ */
  --scroll-width: 300px; /* 可根据需要调整此值 */

  /* ▼▼▼【核心修改 ④】调整渐变色，使其首尾颜色相同，实现真正的无缝 ▼▼▼ */
  background: linear-gradient(
    100deg,
    #333333, #aeaeae, #232323, #aeaeae, #333333
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;

  /* 其他属性会自动继承或复用，无需重复声明 */
  background-repeat: repeat-x;
  background-size: var(--scroll-width) 100%;

  text-shadow:
    0px 1px 1px rgba(255, 255, 255, 0.5),
    0px -1px 1px rgba(0, 0, 0, 0.1);
}


/* 3. 动画定义 */
@keyframes seamless-scroll {
  from {
    background-position: 0 0;
  }
  to {
    /* ▼▼▼【核心修改 ⑤】使用变量设定动画位移，确保其与背景尺寸始终一致 ▼▼▼ */
    background-position: calc(-1 * var(--scroll-width)) 0;
  }
}

/* 4. 响应式调整 (保持不变) */
@media (max-width: 767px) {
  .animated-hero-title {
    font-size: 2.6rem;
    letter-spacing: -1px;
  }
}
/* --- 优化方案结束 --- */
</style>
