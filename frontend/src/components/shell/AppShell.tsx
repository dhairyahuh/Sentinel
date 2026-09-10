import { Outlet } from 'react-router-dom'
import { LoopRail } from './LoopRail'
import { TopBar } from './TopBar'
import { ProvenanceStrip } from './ProvenanceStrip'
import { ErrorBoundary } from '@/components/ui/ErrorBoundary'
import { Tour } from '@/features/tour/Tour'
import { CommandPalette } from '@/features/palette/CommandPalette'

/**
 * The application frame: rail, top bar, route, provenance strip.
 *
 * Fixed to the viewport rather than flowing. This is a console, and a console
 * whose header scrolls away has lost the thing that tells you which run you are
 * looking at. Scroll belongs to the panels that own data.
 *
 * Below 1024px the brief asks for a courteous notice instead of a broken
 * layout. Honoured with a CSS-only breakpoint rather than a resize listener, so
 * there is no reflow thrash on an iPad rotating mid-demo.
 */
export function AppShell() {
  return (
    <>
      <div className="hidden h-screen w-screen flex-col overflow-hidden lg:flex">
        <TopBar />
        <div className="flex min-h-0 flex-1">
          <LoopRail />
          <main className="min-w-0 flex-1 overflow-hidden">
            <ErrorBoundary label="This route">
              <Outlet />
            </ErrorBoundary>
          </main>
        </div>
        <ProvenanceStrip />

        {/* Both live above the routes and outside the error boundary. If a route
            throws, the tour still has to be able to move off it. */}
        <Tour />
        <CommandPalette />
      </div>

      <div className="flex h-screen items-center justify-center p-8 lg:hidden">
        <div className="max-w-sm space-y-3 text-center">
          <h1 className="font-display text-lg font-semibold text-fg">
            Best viewed on a larger display
          </h1>
          <p className="text-sm leading-relaxed text-fg-secondary">
            Sentinel is a financial crime pattern intelligence console — dense network maps, a live transaction feed, and side-by-side detection charts. It needs at least 1024px of width to be readable rather than merely responsive.
          </p>
          <p className="text-xs text-fg-muted">
            The run’s CSV artefacts under <span className="font-mono">artifacts/default_run/</span>{' '}
            contain all underlying data if you prefer to read them directly.
          </p>
        </div>
      </div>
    </>
  )
}
