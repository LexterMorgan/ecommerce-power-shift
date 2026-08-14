import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { loadDashboardData, type DashboardData } from "../lib/dashboardData";

type Ctx = {
  data: DashboardData | null;
  error: string | null;
  loading: boolean;
};

const DashboardContext = createContext<Ctx>({ data: null, error: null, loading: true });

export function DashboardProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData()
      .then(setData)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <DashboardContext.Provider value={{ data, error, loading }}>
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard(): Ctx {
  return useContext(DashboardContext);
}
