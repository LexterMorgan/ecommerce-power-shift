import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { DashboardProvider } from "./lib/DashboardContext";
import { CompetitivePage } from "./pages/CompetitivePage";
import { ExplorerPage } from "./pages/ExplorerPage";
import { OverviewPage } from "./pages/OverviewPage";
import { ScenariosPage } from "./pages/ScenariosPage";
import { SupportingPage } from "./pages/SupportingPage";
import "./styles.css";

export default function App() {
  return (
    <BrowserRouter>
      <DashboardProvider>
        <AppShell>
          <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/competitive" element={<CompetitivePage />} />
            <Route path="/supporting" element={<SupportingPage />} />
            <Route path="/scenarios" element={<ScenariosPage />} />
            <Route path="/explorer" element={<ExplorerPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AppShell>
      </DashboardProvider>
    </BrowserRouter>
  );
}
