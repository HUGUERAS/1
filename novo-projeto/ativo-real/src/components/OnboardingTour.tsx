import { useState, useEffect } from 'react';
import Joyride, { STATUS } from 'react-joyride';
import type { CallBackProps, Step } from 'react-joyride';

interface OnboardingTourProps {
  run?: boolean;
  onFinish?: () => void;
}

export const OnboardingTour = ({ run = true, onFinish }: OnboardingTourProps) => {
  const [runTour, setRunTour] = useState(false);

  useEffect(() => {
    // Check if tour was already completed
    const tourCompleted = localStorage.getItem('onboarding-tour-completed');
    if (!tourCompleted && run) {
      // Wait for elements to be rendered
      setTimeout(() => setRunTour(true), 1000);
    }
  }, [run]);

  const steps: Step[] = [
    {
      target: 'body',
      content: (
        <div>
          <h2 style={{ margin: '0 0 16px 0', color: 'var(--color-primary)' }}>
            🎉 Bem-vindo ao Ativo Real!
          </h2>
          <p style={{ margin: 0, lineHeight: 1.6 }}>
            Vou te mostrar as principais funcionalidades da plataforma. 
            Essa apresentação leva menos de 1 minuto.
          </p>
        </div>
      ),
      placement: 'center',
      disableBeacon: true,
    },
    {
      target: '.dark-mode-toggle',
      content: (
        <div>
          <h3 style={{ margin: '0 0 12px 0', fontSize: '18px' }}>
            🌓 Modo Escuro/Claro
          </h3>
          <p style={{ margin: 0, lineHeight: 1.6 }}>
            Alterne entre os temas claro e escuro conforme sua preferência. 
            Sua escolha é salva automaticamente.
          </p>
        </div>
      ),
      placement: 'left',
    },
    {
      target: '.improved-card',
      content: (
        <div>
          <h3 style={{ margin: '0 0 12px 0', fontSize: '18px' }}>
            👤 Perfis de Usuário
          </h3>
          <p style={{ margin: 0, lineHeight: 1.6 }}>
            Escolha seu perfil para acessar ferramentas específicas:
            <br />• <strong>Topógrafo</strong> - Ferramentas de desenho técnico
            <br />• <strong>Proprietário</strong> - Acompanhamento de regularização
            <br />• <strong>Agricultor</strong> - Gestão de CAR
          </p>
        </div>
      ),
      placement: 'top',
    },
  ];

  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status } = data;
    const finishedStatuses: string[] = [STATUS.FINISHED, STATUS.SKIPPED];

    if (finishedStatuses.includes(status)) {
      setRunTour(false);
      localStorage.setItem('onboarding-tour-completed', 'true');
      if (onFinish) onFinish();
    }
  };

  return (
    <Joyride
      steps={steps}
      run={runTour}
      continuous
      showProgress
      showSkipButton
      callback={handleJoyrideCallback}
      styles={{
        options: {
          arrowColor: 'rgba(0, 31, 63, 0.95)',
          backgroundColor: 'rgba(0, 31, 63, 0.95)',
          overlayColor: 'rgba(0, 5, 9, 0.7)',
          primaryColor: '#CD7F32',
          textColor: '#F0F0F0',
          width: 400,
          zIndex: 10000,
        },
        tooltip: {
          borderRadius: 'var(--radius-xl)',
          padding: 'var(--space-6)',
          fontSize: '16px',
        },
        tooltipContainer: {
          textAlign: 'left',
        },
        buttonNext: {
          backgroundColor: '#CD7F32',
          borderRadius: 'var(--radius-lg)',
          padding: 'var(--space-3) var(--space-6)',
          fontSize: '15px',
          fontWeight: 600,
          transition: 'all 0.2s ease',
        },
        buttonBack: {
          color: '#B0B0B0',
          marginRight: 'var(--space-2)',
        },
        buttonSkip: {
          color: '#B0B0B0',
        },
        beacon: {
          marginTop: '-10px',
          marginLeft: '-10px',
        },
        beaconInner: {
          backgroundColor: '#CD7F32',
        },
        beaconOuter: {
          backgroundColor: 'rgba(205, 127, 50, 0.3)',
          borderColor: '#CD7F32',
        },
      }}
      locale={{
        back: 'Voltar',
        close: 'Fechar',
        last: 'Finalizar',
        next: 'Próximo',
        skip: 'Pular',
      }}
    />
  );
};
