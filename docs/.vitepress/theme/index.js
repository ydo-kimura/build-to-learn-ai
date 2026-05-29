import { h, nextTick, watch } from "vue";
import { useData } from "vitepress";
import DefaultTheme from "vitepress/theme";
import { createMermaidRenderer } from "vitepress-mermaid-renderer";
import "./custom.css";

const enabledToolbarButtons = {
  zoomIn: "enabled",
  zoomOut: "enabled",
  resetView: "enabled",
  copyCode: "enabled",
  toggleFullscreen: "enabled",
  download: "enabled",
};

const toolbarLocales = {
  ja: {
    tooltips: {
      zoomIn: "拡大",
      zoomOut: "縮小",
      resetView: "表示をリセット",
      copyCode: "Mermaidコードをコピー",
      copyCodeCopied: "コピーしました",
      toggleFullscreen: "全画面表示を切り替え",
      download: "図をダウンロード",
      renderErrorText: "図を描画できませんでした",
      toggleErrorDetailsText: "詳細を表示",
      toggleErrorDetailsHideText: "詳細を隠す",
    },
  },
  en: {
    tooltips: {
      zoomIn: "Zoom in",
      zoomOut: "Zoom out",
      resetView: "Reset view",
      copyCode: "Copy Mermaid code",
      copyCodeCopied: "Copied",
      toggleFullscreen: "Toggle fullscreen",
      download: "Download diagram",
      renderErrorText: "Failed to render diagram",
      toggleErrorDetailsText: "Show details",
      toggleErrorDetailsHideText: "Hide details",
    },
  },
};

export default {
  extends: DefaultTheme,
  Layout: () => {
    const { isDark, lang } = useData();

    const initializeMermaid = () => {
      const renderer = createMermaidRenderer({
        theme: isDark.value ? "dark" : "default",
      });

      renderer.setToolbar({
        downloadFormat: "svg",
        fullscreenMode: "browser",
        desktop: {
          ...enabledToolbarButtons,
          zoomLevel: "enabled",
          positions: { vertical: "bottom", horizontal: "right" },
        },
        mobile: {
          ...enabledToolbarButtons,
          zoomLevel: "enabled",
          positions: { vertical: "bottom", horizontal: "right" },
        },
        fullscreen: {
          ...enabledToolbarButtons,
          zoomLevel: "enabled",
          positions: { vertical: "bottom", horizontal: "right" },
        },
        i18n: {
          localeIndex: lang.value === "ja-JP" ? "ja" : "en",
          locales: toolbarLocales,
        },
      });
    };

    nextTick(initializeMermaid);
    watch([isDark, lang], initializeMermaid);

    return h(DefaultTheme.Layout);
  },
};
