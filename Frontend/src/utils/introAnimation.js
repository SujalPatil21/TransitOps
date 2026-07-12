/**
 * Session storage helpers to manage the Landing Page intro animation sequence.
 * Isolates DOM storage calls from React component flows.
 */

const INTRO_PLAYED_KEY = 'transitops_intro_played';

/**
 * Checks if the cinematic introduction sequence has already played during this session.
 * @returns {boolean}
 */
export const hasPlayedIntro = () => {
  try {
    return sessionStorage.getItem(INTRO_PLAYED_KEY) === 'true';
  } catch (e) {
    console.error('SessionStorage access failed:', e);
    return false;
  }
};

/**
 * Marks the introduction sequence as played.
 */
export const markIntroPlayed = () => {
  try {
    sessionStorage.setItem(INTRO_PLAYED_KEY, 'true');
  } catch (e) {
    console.error('SessionStorage write failed:', e);
  }
};

/**
 * Resets the intro played state (mainly for debugging or manual testing).
 */
export const resetIntro = () => {
  try {
    sessionStorage.removeItem(INTRO_PLAYED_KEY);
  } catch (e) {
    console.error('SessionStorage delete failed:', e);
  }
};
