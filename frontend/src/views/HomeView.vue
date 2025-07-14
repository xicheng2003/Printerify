<template>
  <div class="home-view container">
    <section class="hero-section">
      <h2>简单，快速，可靠</h2>
      <p>Printerify，为每一次打印赋能。</p>
    </section>

    <section class="process-section">
      <div class="process-card">
        <Stepper :current-step="state.step" />

        <div class="step-content">
          <!-- Step 1: Upload Document -->
          <div v-if="state.step === 1">
            <h3 class="step-title">第一步：上传您的文档</h3>
            <div class="upload-notice">
              <p><strong>上传须知</strong></p>
              <ul>
                <li><strong>格式推荐</strong>: 为确保打印效果与排版格式一致，强烈建议您上传 <strong>PDF</strong> 格式的文档。</li>
                <li><strong>隐私安全</strong>: 所有文件将通过加密通道上传，并存储在专用服务器上。打印完成后，您的文件将被<strong>立即销毁</strong>，绝不外泄。</li>
                <li><strong>合规声明</strong>: 请遵守相关法律法规，<strong>严禁上传</strong>任何涉密、涉政及其他违禁内容的文件。</li>
              </ul>
            </div>

            <!-- FileUploader is now BEFORE the terms agreement -->
            <FileUploader
              ref="fileUploaderRef"
              @upload-success="onFileUploadSuccess"
              :disabled="!state.agreedToTerms || !state.agreedToPrivacy"
            />

            <!-- Terms Agreement Section is now AFTER the file uploader -->
            <div class="terms-agreement">
              <div>
                <input type="checkbox" id="terms" v-model="state.agreedToTerms" />
                <label for="terms">
                  我已阅读并同意
                  <a href="#" @click.prevent="state.showTermsModal = true">《Printerify 服务条款》</a>
                </label>
              </div>
              <div>
                <input type="checkbox" id="privacy" v-model="state.agreedToPrivacy" />
                <label for="privacy">
                  我已阅读并同意
                  <a href="#" @click.prevent="state.showPrivacyModal = true">《Printerify 隐私协议》</a>
                </label>
              </div>
            </div>
          </div>

          <!-- Step 2: Print Options -->
          <div v-if="state.step === 2">
             <h3 class="step-title">第二步：设置打印选项</h3>
            <div class="options-grid">
              <div>
                <label>纸张大小:</label>
                <input type="text" :value="state.options.paper_size" disabled />
              </div>
              <div>
                <label>色彩:</label>
                <input type="text" :value="state.options.color" disabled />
              </div>
              <div>
                <label>打印模式:</label>
                <select v-model="state.options.sided" :disabled="state.isLoading">
                  <option>单面</option>
                  <option>双面</option>
                  <option>单双（即首页封面为单面打印，其余内容双面打印）</option>
                </select>
              </div>
              <div>
                <label>份数:</label>
                <input type="number" v-model.number="state.options.copies" min="1" :disabled="state.isLoading"/>
              </div>
              <div>
                <label>装订方式:</label>
                <select v-model="state.options.binding_method" :disabled="state.isLoading">
                  <option>无装订</option>
                  <option>订书钉装订</option>
                </select>
              </div>
              <div v-if="state.options.binding_method === '订书钉装订'">
                <label>装订位置:</label>
                <select v-model="state.options.binding_detail" :disabled="state.isLoading">
                  <option>左上角装订</option>
                  <option>左侧装订</option>
                </select>
              </div>
            </div>
            <div class="pricing-rules">
              <p><strong>计费规则说明</strong></p>
              <ul>
                <li>打印费用: 单面打印 0.15元/页，双面打印 0.30元/页 (即每面0.15元)。</li>
                <li>装订服务: 若选择装订，将额外收取 0.10元/本。</li>
                <li>基础服务费: 每笔订单将收取 0.50元 的基础服务费。</li>
              </ul>
            </div>
            <BaseButton @click="handlePriceQuote" :loading="state.isLoading" class="full-width-btn">计算价格</BaseButton>
          </div>

          <!-- Step 3: Payment -->
          <div v-if="state.step === 3">
            <h3 class="step-title">第三步：确认价格并支付</h3>
            <div class="price-result" v-if="state.priceQuote">
              <p>预估页数: <strong>{{ state.priceQuote.estimated_pages }}</strong> 页</p>
              <p class="price">预估价格: <strong>¥ {{ state.priceQuote.estimated_price.toFixed(2) }}</strong></p>
            </div>

            <div class="payment-method-selector">
              <label :class="{ 'active': state.paymentMethod === 'WECHAT' }">
                <input type="radio" v-model="state.paymentMethod" value="WECHAT" name="payment-method"/>
                <img src="/wechat-logo.png" alt="微信支付" class="payment-button-image"/>
              </label>
              <label :class="{ 'active': state.paymentMethod === 'ALIPAY' }">
                <input type="radio" v-model="state.paymentMethod" value="ALIPAY" name="payment-method"/>
                <img src="/alipay-logo.png" alt="支付宝" class="payment-button-image"/>
              </label>
            </div>

            <div class="payment-section">
              <div v-if="state.paymentMethod === 'WECHAT'">
                <p class="payment-instruction">请使用微信扫描下方二维码完成支付</p>
                <img src="/wechat_qr.jpg" alt="微信收款二维码" class="qr-code">
              </div>
              <div v-if="state.paymentMethod === 'ALIPAY'">
                 <p class="payment-instruction">请使用支付宝扫描二维码，或点击下方链接</p>
                 <img src="/alipay_qr.jpg" alt="支付宝收款二维码" class="qr-code">
                 <a href="https://qr.alipay.com/2m611064ovvydd9jbdrnv22" target="_blank" class="payment-link">
                   点此跳转支付宝APP付款
                 </a>
              </div>
              <PaymentUploader @upload-success="onScreenshotUploaded" />
            </div>

            <div class="form-group">
              <label>请输入手机号以完成下单：</label>
              <input type="tel" v-model="state.phoneNumber" placeholder="用于查询订单" :disabled="state.isLoading" />
            </div>
            <BaseButton @click="handleCreateOrder" :loading="state.isLoading" :disabled="!state.screenshotId" class="full-width-btn">
              我已支付，确认下单
            </BaseButton>
          </div>

          <!-- Step 4: Completion -->
          <div v-if="state.step === 4" class="completion-view">
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            <h3 class="step-title">订单提交成功！</h3>
            <p>取件时请出示取件码，请牢记或截图保存。</p>
            <p>凭手机号和取件码，可在订单查询页面查询订单状态</p>
            <div class="pickup-code-wrapper">
              <span class="pickup-code-label">您的取件码</span>
              <strong class="pickup-code">{{ state.finalOrder.pickup_code }}</strong>
            </div>
            <p class="order-number-info">完整订单号: {{ state.finalOrder.order_number }}</p>
            <BaseButton @click="reset" class="full-width-btn">再来一单</BaseButton>
          </div>
        </div>

        <p v-if="state.errorMessage" class="error-message">{{ state.errorMessage }}</p>
      </div>
    </section>
  </div>

  <!-- Modals Teleported to body -->
  <Teleport to="body">
    <Modal :show="state.showTermsModal" @close="state.showTermsModal = false">
      <template #header><h3>服务条款</h3></template>
      <template #body>
        <pre class="terms-text">
<strong>最后更新日期：2025年7月14日</strong>

<strong>引言与协议接受</strong>
欢迎使用 Printerify（以下简称“本服务”）。本服务条款构成您（以下简称“用户”）与 Printerify（以下简称“我们”）之间具有法律约束力的协议。在访问或使用本服务之前，请您务必仔细阅读并充分理解本条款的全部内容。您通过访问服务页面、上传文件、下单或任何其他方式使用本服务，即表示您已阅读、理解并同意接受本条款所有内容的约束。若您不同意本条款的任何内容，请立即停止使用本服务。

<strong>服务描述</strong>
Printerify 为您提供一个便捷的在线平台，允许您上传需要打印的数字文件，自定义打印规格（如纸张类型、尺寸、颜色等），提交订单，并通过指定的支付方式完成付款。订单完成后，您将获得一个唯一的取件码，凭此码在指定地点领取您的实体打印成品。我们致力于提供高质量的打印服务，但 Printerify 保留根据运营需求随时修改、暂停或永久终止部分或全部服务的权利。若发生此类变动，我们将尽力通过网站公告等形式提前通知用户。

<strong>用户行为与内容规范</strong>
用户承诺在使用本服务时，将严格遵守所有适用的法律法规。您对通过本服务上传、提交或分享的所有文件、数据及信息（以下统称为“用户内容”）负有完全的法律责任。您必须保证，您所上传的用户内容拥有合法的知识产权，或已获得相关权利人的充分授权，不会侵犯任何第三方的版权、商标权、专利权、肖像权、隐私权或其他合法权益。严禁用户利用本服务上传、打印或传播任何包含非法、淫秽色情、暴力、恐怖、赌博、诽谤、骚扰、种族歧视或任何其他违反法律、道德及社会公序良俗的内容。Printerify 有权单方面判断用户内容是否违反本条款，并无需通知即可拒绝打印、删除相关内容，并视情节严重程度，暂停或永久终止向该用户提供服务。

<strong>订单、支付与交付</strong>
本服务的订单流程、具体价格计算方式以及可接受的支付渠道均以网站页面实时显示为准。您在提交订单前，请仔细核对订单详情，包括打印规格、数量和总金额。订单一旦提交，即表示您确认了订单内容。Printerify 将根据您上传的支付凭证来核实付款状态，并在确认付款后开始处理您的订单。我们会尽力确保打印质量，但由于设备、耗材及文件本身等因素，打印成品可能存在合理的色彩、尺寸误差，此不属于质量问题。若因 Printerify 的设备或操作失误导致严重的打印质量问题，我们将根据具体情况为您提供重印或退款服务。订单完成后生成的取件码是您领取打印成品的唯一凭证，请务必妥善保管，因您个人保管不善导致的任何损失，由您自行承担。

<strong>知识产权</strong>
Printerify 尊重并保护知识产权。您上传至本服务的用户内容的知识产权，仍归您或原始权利人所有。您仅授予我们一项非独家的、为履行打印订单之目的所必需的权利，来使用、复制和处理您的用户内容。订单履行完毕后，此授权自动终止。与此同时，Printerify 网站本身所包含的所有内容，包括但不限于Logo、商标、文字、图形、界面设计、代码、算法和软件的知识产权，均归我们所有，受相关法律保护。未经我们书面许可，任何个人或组织不得以任何形式进行复制、修改、传播或用于任何商业目的。

<strong>免责声明与责任限制</strong>
在适用法律允许的最大范围内，本服务及其所有内容均是“按现状”和“按可用状态”提供的，Printerify 不作任何形式的明示或暗示的保证，包括但不限于服务的稳定性、可靠性、准确性或特定用途的适用性。对于因不可抗力、第三方服务（如网络中断）、系统维护或用户自身原因（如上传了格式错误、内容有误、分辨率过低的文件）导致的任何服务中断或打印质量问题，我们不承担责任。在任何情况下，我们因履行本条款而产生的全部赔偿责任，累计总额不应超过您为引起该责任的特定订单所支付的费用总额。

<strong>协议的终止</strong>
如果用户违反本服务条款中的任何规定，Printerify 有权随时单方面中断或终止向该用户提供服务，而无需事先通知。用户也可以随时停止使用本服务，以终止本协议。协议终止后，我们不再有义务为用户提供任何服务，但用户在使用服务期间应尽的义务（如保密、知识产权、赔偿等）不因协议终止而免除。

<strong>条款的修订</strong>
我们保留根据业务发展和法律法规变化，不时修订本服务条款的权利。条款更新后，我们将在网站的显著位置发布公告，以通知用户。修订后的条款自发布之日起生效。若您在条款修订后继续使用 Printerify 的服务，即表示您已接受并同意遵守更新后的条款。

<strong>法律适用与争议解决</strong>
本条款的订立、生效、解释、履行及争议解决，均适用中华人民共和国（不含港澳台地区）的法律。因本条款产生的或与本条款有关的任何争议，双方应首先尝试通过友好协商解决。如果协商不成，任何一方均有权将争议提交至 Printerify 服务提供方所在地有管辖权的人民法院通过诉讼解决。
        </pre>
      </template>
    </Modal>

    <Modal :show="state.showPrivacyModal" @close="state.showPrivacyModal = false">
      <template #header><h3>隐私协议</h3></template>
      <template #body>
        <pre class="terms-text">
<strong>最后更新日期：2025年7月14日</strong>

<strong>引言</strong>
Printerify（以下简称“我们”）深知个人信息对您的重要性，并承诺将依据法律法规，采取严格的安全保护措施，全力保护您的个人信息及隐私安全。本隐私协议旨在向您清晰地说明，在您使用我们的在线打印服务过程中，Printerify 如何收集、使用、存储、共享和保护您的个人信息，以及您所享有的相关权利。请您在使用本服务前，仔细阅读并确认您已经充分理解本协议所写明的内容。

<strong>我们收集的信息类型</strong>
为了向您提供完整、优质的打印服务，Printerify 会根据合法、正当、必要的原则，收集以下与您相关的信息。
首先，是您为履行订单而主动提供的个人身份与联络信息，主要指您的手机号码，我们将用其与您进行订单相关的沟通。
其次，是您为实现打印目的而上传的用户内容，即您希望打印的数字文件（如PDF、Word文档、图片等）。
再次，当您选择特定支付方式时，我们可能会收集您上传的支付凭证截图，用以核实您的付款状态。
最后，为了维护和改进我们的服务，Printerify 可能会自动收集一些技术与日志信息，例如您的IP地址、浏览器类型、操作系统、访问服务的日期与时间，以及您的操作记录等。这些信息通常是匿名的，无法直接关联到您的个人身份。

<strong>我们如何使用您的信息</strong>
Printerify 严格遵守法律法规的规定及与您的约定，将收集到的信息用于以下明确、具体的目的。
最主要的使用目的是履行您的打印订单，我们会处理您上传的文件并使用您的手机号码，以便在订单状态变更（如打印完成、可供取件）时与您取得联系。
同时，我们会使用您的支付凭证来确认订单款项是否到账，以启动订单处理流程。
此外，我们会对收集到的匿名化技术与日志信息进行分析，用于监控服务运行状态、排查故障、优化网站性能和用户体验，从而为您提供更稳定、更便捷的服务。

<strong>信息的共享与披露</strong>
我们对您的信息负有保密义务，并承诺绝不会将您的个人信息或您上传的打印文件出售、出租或以任何其他形式与任何无关的第三方进行交易。我们仅在以下少数、必要的情况下，才会共享或披露您的信息。
一是为实现打印目的，我们可能会将您的文件提供给 Printerify 内部负责打印操作的人员。
二是在获得您明确、单独的同意后，我们可能会在您同意的范围内共享信息。
三是根据适用的法律法规、法律程序的要求、强制性的行政或司法要求，我们可能有义务对外提供您的信息。在符合法律法规的前提下，当我们收到上述披露信息的请求时，会要求对方必须出具与之相应的法律文件。

<strong>数据安全</strong>
Printerify 已采取了符合业界标准、合理可行的物理、技术及行政管理上的安全措施，来保护您提供的信息，防止数据遭到未经授权的访问、公开披露、使用、修改、损坏或丢失。例如，我们使用SSL加密技术对数据传输过程进行保护；我们部署了严格的访问控制机制，确保只有授权人员才可访问个人信息；我们会举办安全和隐私保护培训课程，加强员工对于保护信息重要性的认识。尽管我们已采取上述措施，但请您理解，由于技术的限制以及可能存在的各种恶意手段，在互联网行业，不可能始终保证信息百分之百的安全。

<strong>数据保留</strong>
我们只在为实现本协议所述目的所必需的期限内，以及法律法规所要求的时限内保留您的个人信息。对于您为打印而上传的文件及支付凭证，Printerify 承诺，在您的订单完成（即您成功取件或订单关闭）后的30天内，将从我们的服务器上进行永久性、不可恢复的删除，以最大限度地保护您的隐私。您的订单记录及关联的手机号码等信息，将为遵守相关法律规定（如电子商务法）及处理潜在纠纷的需要，保留更长的时间。

<strong>用户的权利</strong>
根据相关法律法规，我们保障您对自己的个人信息行使以下权利：您有权访问、更正或补充您的信息。考虑到本服务的性质，您对上传文件的主要管理权限体现在下单前的修改与删除。对于您的个人信息，如需行使访问、更正或请求删除的权利，您可以通过我们提供的联系方式与 Printerify 沟通。在核实您的身份后，我们将响应您的请求。

<strong>儿童隐私</strong>
我们的服务主要面向成年人。Printerify 不会在知情的情况下，收集未满14周岁（或您所在司法辖区规定的其他年龄）儿童的个人信息。如果我们发现自己在无意中收集了儿童的个人信息，我们会设法尽快删除相关数据。

<strong>协议的更新</strong>
Printerify 的隐私协议可能会根据服务的变更和法律法规的要求适时进行更新。未经您明确同意，我们不会削减您按照本隐私协议所应享有的权利。任何更新我们都会在网站上发布修订后的版本，并以公告形式通知您。对于重大变更，我们还会提供更为显著的通知。

<strong>联系我们</strong>
如果您对本隐私协议有任何疑问、意见或建议，或者希望行使您的用户权利，欢迎随时通过以下方式与我们联系：
电子邮箱：xicheng.lin@foxmail.com
我们将尽快审核所涉问题，并在验证您的用户身份后的十五个工作日内予以回复。
        </pre>
      </template>
    </Modal>
  </Teleport>

</template>

<script setup>
import { reactive, ref } from 'vue';
import api from '@/services/apiService';

import Stepper from '@/components/Stepper.vue';
import FileUploader from '@/components/FileUploader.vue';
import PaymentUploader from '@/components/PaymentUploader.vue';
import BaseButton from '@/components/BaseButton.vue';
import Modal from '@/components/Modal.vue'; // Make sure you have this component

const fileUploaderRef = ref(null);

const state = reactive({
  step: 1,
  file: null,
  fileId: null,
  options: {
    paper_size: 'A4',
    color: '黑白',
    sided: '单面',
    copies: 1,
    binding_method: '无装订',
    binding_detail: '',
  },
  phoneNumber: '',
  priceQuote: null,
  screenshotId: null,
  finalOrder: null,
  isLoading: false,
  errorMessage: '',
  paymentMethod: 'WECHAT',
  // State for terms and modals
  agreedToTerms: false,
  agreedToPrivacy: false,
  showTermsModal: false,
  showPrivacyModal: false,
});

function onFileUploadSuccess(payload) {
  state.file = payload.file;
  state.fileId = payload.id;
  state.step = 2;
}

function onScreenshotUploaded(uploadedId) {
  state.screenshotId = uploadedId;
}

async function handlePriceQuote() {
  if (state.options.binding_method === '订书钉装订' && !state.options.binding_detail) {
    state.options.binding_detail = '左上角装订';
  }
  if (state.options.binding_method === '无装订') {
    state.options.binding_detail = '';
  }

  state.isLoading = true;
  state.errorMessage = '';
  try {
    const response = await api.getPriceQuote(state.file, state.options);
    state.priceQuote = response.data;
    state.step = 3;
  } catch (error) {
    state.errorMessage = '计价失败，请稍后重试。';
    console.error(error);
  } finally {
    state.isLoading = false;
  }
}

async function handleCreateOrder() {
  if (!state.phoneNumber) {
    state.errorMessage = '请输入手机号！';
    return;
  }
  if (!state.screenshotId) {
    state.errorMessage = '请先上传付款截图！';
    return;
  }

  state.isLoading = true;
  state.errorMessage = '';
  try {
    const orderData = {
      phone_number: state.phoneNumber,
      specifications: state.options,
      file_ids: [state.fileId],
      payment_screenshot_id: state.screenshotId,
      payment_method: state.paymentMethod,
    };
    const response = await api.createOrder(orderData);
    state.finalOrder = response.data;
    state.step = 4;
    state.isLoading = false;
  } catch (error) {
    console.error("Initial order creation failed, starting verification process:", error);

    // 出现错误时不立即报错，而是启动验证流程
    // 延迟2秒，给后端足够的时间处理订单
    setTimeout(async () => {
      try {
        // **修正点**: 根据您的apiService.js，现在我们只传递手机号进行查询
        const verificationResponse = await api.queryOrder(state.phoneNumber);

        // 假设API返回一个按时间倒序排列的订单数组
        if (verificationResponse.data && verificationResponse.data.length > 0) {
          const latestOrder = verificationResponse.data[0];
          const orderCreationTime = new Date(latestOrder.created_at);
          const now = new Date();
          const timeDiffSeconds = (now - orderCreationTime) / 1000;

          // 如果最新订单是在过去30秒内创建的，我们就认为是刚刚下单成功的
          if (timeDiffSeconds < 30) {
            state.finalOrder = latestOrder;
            state.step = 4;
          } else {
            // 如果订单太旧，说明新订单确实没创建成功
            state.errorMessage = '订单创建失败，请稍后重试或联系客服。';
          }
        } else {
          // 如果用手机号查不到任何订单，那肯定就是失败了
          state.errorMessage = '订单创建失败，未找到相关订单记录。';
        }
      } catch (verificationError) {
        console.error("Order verification also failed:", verificationError);
        state.errorMessage = '订单状态验证失败，请检查网络或联系客服。';
      } finally {
        // 无论验证成功与否，都要结束加载状态
        state.isLoading = false;
      }
    }, 2000); // 延迟2秒执行
  }
}

function reset() {
  Object.assign(state, {
    step: 1, file: null, fileId: null, priceQuote: null, finalOrder: null,
    phoneNumber: '', screenshotId: null, errorMessage: '',
    options: { paper_size: 'A4', color: '黑白', sided: '单面', copies: 1, binding_method: '无装订', binding_detail: '' },
    paymentMethod: 'WECHAT',
    // Reset terms state
    agreedToTerms: false,
    agreedToPrivacy: false,
    showTermsModal: false,
    showPrivacyModal: false,
  });
  if (fileUploaderRef.value) {
    fileUploaderRef.value.reset();
  }
}
</script>

<style scoped>
/* Your existing styles... */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}
.hero-section { text-align: center; padding: 2rem 0; margin-bottom: 2rem; }
.hero-section h2 { font-size: 2.5rem; font-weight: 700; color: #1e293b; }
.hero-section p { font-size: 1.125rem; color: #64748b; }
.process-section { padding-bottom: 2rem; }
.process-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 1.5rem 2.5rem;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -4px rgba(0,0,0,.1);
  border: 1px solid #e2e8f0;
}
.step-title { font-size: 1.5rem; font-weight: 600; text-align: center; margin-bottom: 2rem; color: var(--text-dark); }
.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.options-grid div { display: flex; flex-direction: column; }
.options-grid label { margin-bottom: 0.5rem; font-weight: 500; color: var(--text-dark); }
.price-result { background: #f0f4ff; border: 1px solid #c7d2fe; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center; }
.price { font-size: 1.75rem; color: var(--primary-color); font-weight: 700; }
.payment-section { border-top: 1px solid var(--border-color); padding: 1.5rem 0; margin-top: 1.5rem; text-align: center; }
.payment-instruction { margin-top: 0; color: #334155; }
.qr-code { max-width: 180px; margin: 1rem auto; display: block; border-radius: 8px; }
.form-group { margin-top: 1.5rem; margin-bottom: 1.5rem; }
.form-group label { margin-bottom: 0.5rem; font-weight: 500; }
.full-width-btn { width: 100%; padding: 0.875rem; font-size: 1.1rem; }
.completion-view { text-align: center; padding: 2rem 0; }
.completion-view > p { color: #64748b; margin-bottom: 1rem; }
.pickup-code-wrapper { background-color: #f0f4ff; border: 1px dashed var(--primary-color); padding: 1rem; border-radius: 8px; margin: 1.5rem auto; max-width: 300px; }
.pickup-code-label { font-size: 1rem; color: #475569; }
.pickup-code { display: block; font-size: 2.5rem; font-weight: 700; color: var(--primary-color); letter-spacing: 4px; margin-top: 0.5rem; }
.error-message { color: #ef4444; font-weight: 500; margin-top: 1.5rem; text-align: center; background-color: rgba(239, 68, 68, 0.1); padding: 0.75rem; border-radius: 8px;}
.order-number-info { color: #94a3b8; font-size: 0.875rem; margin-top: -0.5rem; margin-bottom: 2rem; }
.pricing-rules, .upload-notice {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: #495057;
}
.pricing-rules p, .upload-notice p { margin: 0 0 0.75rem 0; font-weight: 600; color: var(--text-dark); }
.pricing-rules ul, .upload-notice ul { list-style-type: none; padding-left: 0; }
.pricing-rules li, .upload-notice li { margin-bottom: 0.5rem; position: relative; padding-left: 1.25rem; }
.pricing-rules li::before, .upload-notice li::before {
  content: '•';
  color: var(--primary-color);
  font-weight: bold;
  display: inline-block;
  position: absolute;
  left: 0;
  top: 0;
}
.pricing-rules li:last-child, .upload-notice li:last-child { margin-bottom: 0; }
.upload-notice li strong { color: #c2410c; }

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
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 4px;
  transition: all 0.2s ease-in-out;
  width: 160px;
  height: 56px;
  box-sizing: border-box;
}
.payment-method-selector label:hover {
  border-color: #c7d2fe;
}
.payment-method-selector label.active {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}
.payment-method-selector input[type="radio"] {
  display: none;
}
.payment-button-image {
  display: block;
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}
.payment-link {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: #1677ff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: 500;
  transition: background-color 0.2s;
}
.payment-link:hover {
  background-color: #4096ff;
}

/* Styles for the agreement section and modal text */
.terms-agreement {
  font-size: 0.9rem;
  color: #666;
  margin-top: 2rem; /* Added margin-top to separate from uploader */
  margin-bottom: 0; /* Removed bottom margin as it's the last element */
  padding: 1rem;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
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
  color: var(--primary-color);
  text-decoration: underline;
  cursor: pointer;
}
.terms-text {
  white-space: pre-wrap;
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.5;
  text-align: left;
  color: #333;
}

@media (max-width: 767px) {
  .hero-section h2 { font-size: 2rem; }
  .hero-section p { font-size: 1rem; }
  .step-title { font-size: 1.25rem; }
  .process-card { padding: 1.5rem 1rem; }
  .options-grid { grid-template-columns: 1fr; }
  .pickup-code { font-size: 2rem; }
  .payment-method-selector { gap: 1rem; }
  .payment-method-selector label { width: 140px; height: 48px; }
}
</style>
